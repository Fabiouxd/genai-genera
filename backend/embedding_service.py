import voyageai
from supabase import create_client
import os
import time
from dotenv import load_dotenv

load_dotenv()

voyage_client = voyageai.Client(api_key=os.getenv("VOYAGE_API_KEY"))
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

def gerar_embedding(texto: str) -> list:
    resposta = voyage_client.embed(
        [texto],
        model="voyage-3-lite",
        input_type="document"
    )
    return resposta.embeddings[0]


def dividir_em_chunks(dados_json: dict) -> list:
    chunks = []

    if dados_json.get("resumo_executivo"):
        chunks.append({
            "tipo": "resumo",
            "texto": f"Resumo do relatório: {dados_json['resumo_executivo']}"
        })

    if dados_json.get("ancestralidade"):
        anc = dados_json["ancestralidade"]
        texto_anc = f"Ancestralidade: {anc.get('descricao_geral', '')}. "
        if anc.get("regioes"):
            regioes = ", ".join([
                f"{r['nome']} ({r['percentual']})"
                for r in anc["regioes"] if r.get("nome")
            ])
            texto_anc += f"Regiões de origem: {regioes}"
        chunks.append({"tipo": "ancestralidade", "texto": texto_anc})

    for pred in dados_json.get("predisposicoes", []):
        if not pred:
            continue
        texto_pred = (
            f"Predisposição para {pred.get('condicao', '')}: "
            f"risco {pred.get('risco', '')}. "
            f"Gene: {pred.get('gene', 'não especificado')}. "
            f"Variante: {pred.get('variante', 'não especificado')}. "
            f"Explicação: {pred.get('explicacao_simples', '')}. "
            f"Recomendação: {pred.get('recomendacao', '')}"
        )
        chunks.append({"tipo": "predisposicao", "texto": texto_pred})

    for var in dados_json.get("variantes_destaque", []):
        if not var:
            continue
        texto_var = (
            f"Variante no gene {var.get('gene', '')}: "
            f"{var.get('variante', '')}. "
            f"Classificação: {var.get('classificacao', '')}. "
            f"Significado: {var.get('explicacao_simples', '')}"
        )
        chunks.append({"tipo": "variante", "texto": texto_var})

    recs = dados_json.get("recomendacoes_gerais", [])
    if recs:
        texto_rec = "Recomendações gerais: " + ". ".join(
            [r for r in recs if r]
        )
        chunks.append({"tipo": "recomendacoes", "texto": texto_rec})

    return chunks


def salvar_relatorio_completo(dados_json: dict, texto_bruto: str) -> str:
    paciente = dados_json.get("paciente", {})
    resultado = supabase.table("relatorios").insert({
        "nome_paciente": paciente.get("nome", "Paciente"),
        "data_exame": paciente.get("data_exame", ""),
        "conteudo_json": dados_json,
        "texto_bruto": texto_bruto
    }).execute()

    relatorio_id = resultado.data[0]["id"]
    print(f"Relatório salvo com ID: {relatorio_id}")

    chunks = dividir_em_chunks(dados_json)
    print(f"Gerando embeddings para {len(chunks)} chunks...")

    for i, chunk in enumerate(chunks):
        print(f"  Chunk {i+1}/{len(chunks)}: {chunk['tipo']}")
        embedding = gerar_embedding(chunk["texto"])
        supabase.table("chunks_relatorio").insert({
            "relatorio_id": relatorio_id,
            "texto": chunk["texto"],
            "embedding": embedding
        }).execute()

        # Pausa para respeitar limite de 3 req/min do plano gratuito
        if i < len(chunks) - 1:
            print(f"  Aguardando 20s... ({i+1}/{len(chunks)} concluídos)")
            time.sleep(20)

    print("Todos os chunks salvos!")
    return relatorio_id