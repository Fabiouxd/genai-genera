import anthropic
import json
import os
from dotenv import load_dotenv

load_dotenv()

def estruturar_relatorio(texto_bruto: str) -> dict:
    client = anthropic.Anthropic(
        api_key=os.getenv("ANTHROPIC_API_KEY")
    )
    
    prompt = f"""Você é um especialista em genética médica e vai analisar 
um relatório genético extraído de um PDF.

Sua tarefa é organizar as informações em um JSON estruturado.

REGRAS IMPORTANTES:
- Retorne APENAS o JSON, sem nenhum texto antes ou depois
- Não use markdown, não use ```json, apenas o JSON puro
- Se uma informação não existir no relatório, use null
- Mantenha explicacoes_simples em linguagem que qualquer pessoa entenda
- Para o campo risco, use apenas: "alto", "medio" ou "baixo"
- Se o documento não for um relatório genético, estruture as informações
  principais que conseguir identificar no formato solicitado

RELATÓRIO PARA ANALISAR:
{texto_bruto}

FORMATO DO JSON QUE VOCÊ DEVE RETORNAR:
{{
  "paciente": {{
    "nome": "",
    "data_nascimento": "",
    "data_exame": "",
    "codigo_amostra": ""
  }},
  "ancestralidade": {{
    "descricao_geral": "",
    "regioes": [
      {{ "nome": "", "percentual": "" }}
    ]
  }},
  "predisposicoes": [
    {{
      "condicao": "",
      "risco": "alto|medio|baixo",
      "gene": "",
      "variante": "",
      "explicacao_simples": "",
      "recomendacao": ""
    }}
  ],
  "variantes_destaque": [
    {{
      "gene": "",
      "variante": "",
      "classificacao": "",
      "significado_clinico": "",
      "explicacao_simples": ""
    }}
  ],
  "recomendacoes_gerais": [],
  "resumo_executivo": ""
}}"""

    try:
        mensagem = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        texto_resposta = mensagem.content[0].text
        
        texto_limpo = texto_resposta.strip()
        if texto_limpo.startswith("```"):
            linhas = texto_limpo.split("\n")
            texto_limpo = "\n".join(linhas[1:-1])
        
        dados_estruturados = json.loads(texto_limpo)
        
        return {"sucesso": True, "dados": dados_estruturados}
    
    except json.JSONDecodeError as erro:
        return {"sucesso": False, "erro": f"Erro ao interpretar JSON: {str(erro)}", "dados": None}
    
    except Exception as erro:
        return {"sucesso": False, "erro": str(erro), "dados": None}