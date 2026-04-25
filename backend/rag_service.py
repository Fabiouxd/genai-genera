import anthropic
import voyageai
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

anthropic_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
voyage_client = voyageai.Client(api_key=os.getenv("VOYAGE_API_KEY"))
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

def buscar_chunks_relevantes(pergunta: str, relatorio_id: str) -> list:
    """
    Converte a pergunta em embedding e busca os trechos
    mais relevantes do relatório no banco de dados.
    """
    
    # Converte a pergunta em vetor numérico
    # Usamos input_type="query" para perguntas (diferente de "document" para textos)
    resposta = voyage_client.embed(
        [pergunta],
        model="voyage-3-lite",
        input_type="query"
    )
    embedding_pergunta = resposta.embeddings[0]
    
    # Busca os 5 chunks mais similares no banco
    resultado = supabase.rpc("buscar_similares", {
        "query_embedding": embedding_pergunta,
        "relatorio_id": relatorio_id,
        "limite": 5
    }).execute()
    
    return resultado.data


def responder_pergunta(pergunta: str, relatorio_id: str) -> dict:
    """
    Recebe uma pergunta e o ID do relatório,
    busca o contexto relevante e retorna a resposta da IA.
    """
    
    # Passo 1: busca os trechos mais relevantes do relatório
    chunks = buscar_chunks_relevantes(pergunta, relatorio_id)
    
    if not chunks:
        return {
            "resposta": "Não encontrei informações suficientes no relatório para responder essa pergunta.",
            "chunks_usados": 0
        }
    
    # Passo 2: monta o contexto com os trechos encontrados
    contexto = "\n\n".join([c["texto"] for c in chunks])
    
    # Passo 3: monta o prompt com instruções claras para o Claude
    sistema = """Você é um assistente de saúde especializado em explicar 
relatórios médicos e genéticos em linguagem simples e acolhedora.

SUAS REGRAS:
- Use APENAS as informações do contexto fornecido para responder
- Explique em linguagem clara que qualquer pessoa entenda
- Seja empático e acolhedor — o usuário pode estar ansioso
- Se a informação não estiver no contexto, diga claramente que não encontrou
- NUNCA faça diagnósticos médicos
- NUNCA prescreva medicamentos ou doses
- Sempre sugira consultar um médico para decisões clínicas importantes
- Responda em português brasileiro
- Seja objetivo mas completo — nem muito curto nem muito longo"""

    mensagem = anthropic_client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=600,
        system=sistema,
        messages=[
            {
                "role": "user",
                "content": f"""CONTEXTO DO RELATÓRIO:
{contexto}

PERGUNTA DO USUÁRIO:
{pergunta}

Responda de forma clara e acolhedora baseando-se apenas no contexto acima."""
            }
        ]
    )
    
    return {
        "resposta": mensagem.content[0].text,
        "chunks_usados": len(chunks)
    }