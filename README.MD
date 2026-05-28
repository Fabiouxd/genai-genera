# GenAI Genera — Interprete Inteligente de Relatorios Geneticos

Challenge Dasa + Genera — FIAP 2026

Grupo: Fabio Mendes, Bernardo Rupolo, Marcos Vinicius dos Santos Morgado, Leonardo Magalhaes

---

## O Problema

O Genera (Dasa) entrega ao paciente um relatorio genetico em PDF com dezenas de paginas repletas de termos extremamente tecnicos, como: "Polimorfismo rs429358 no gene APOE — alelo e4 detectado". Para um paciente comum, esse documento e incompreensivel. O resultado pratico e que o PDF vai para a gaveta, nenhuma mudanca de habito preventivo acontece e o valor do exame e desperdicado. O problema nao esta no conteudo — esta na ausencia de uma camada inteligente que o traduza para o paciente de forma humana e acionavel.

---

## A Solucao

O GenAI Genera e uma plataforma web que transforma relatorios geneticos complexos em uma experiencia interativa, segura e totalmente acessivel. Ao realizar o upload do arquivo PDF, o paciente consegue:

* Resumo Simplificado: Traducao dos termos tecnicos para uma linguagem leiga e direta.
* Dashboard de Riscos: Visualizacao dos principais riscos geneticos organizados por prioridade.
* Chatbot Especialista (RAG): Uma IA contextualizada que responde duvidas baseando-se estritamente no relatorio do usuario.
* Prevencao Personalizada: Recomendacoes de habitos e proximos passos focados em bem-estar e saude preventiva.

---

## Pipeline da Solucao

[ PDF Upload ] 
       │
       ▼
[ Extracao de Texto ] ──> (pdfplumber)
       │
       ▼
[ Estruturacao em JSON ] ──> (Claude AI)
       │
       ▼
[ Geracao de Embeddings ] ──> (Voyage AI: voyage-3-lite)
       │
       ▼
[ Armazenamento Vetorial ] ──> (Supabase + pgvector)
       │
 ┌─────┴────────────────────────┐
 │ Pergunta do Usuario          │
 │     │                        │
 │     ▼                        │
 │ [ Busca Semantica ]          │
 │     │                        │
 │     ▼                        │
 │ [ Resposta Contextualizada ] ──> (Claude Haiku) ──> [ Interface Next.js ]
 └──────────────────────────────┘

---

## Arquitetura de IA — Sistema RAG

A tecnica central do projeto e o RAG (Retrieval-Augmented Generation), que garante que as respostas do chatbot sejam sempre fundamentadas nos dados reais do relatorio do paciente, mitigando o risco de alucinacoes da IA.

* Como Funciona: O relatorio processado e dividido em chunks (trechos) semanticos. Cada chunk e convertido em um vetor numerico (embedding) de 512 dimensoes pelo Voyage AI e armazenado no Supabase via extensao pgvector. Quando o usuario interage com o chat, a pergunta tambem e vetorizada. O sistema realiza uma busca por similaridade vetorial e recupera os 5 trechos mais relevantes do relatorio. Esses trechos sao injetados como contexto junto a pergunta para o Claude, que gera a resposta final.

* Componentes de Tecnologia: O modelo de linguagem utilizado e o Claude Haiku (Anthropic), escolhido pela alta precisao na interpretacao de textos medicos, excelente aderencia a system prompts restritivos e custo-beneficio ideal para escala academico. O modelo de embeddings e o voyage-3-lite (Voyage AI), parceiro oficial da Anthropic, otimizado para recuperacao de texto e com otima performance em lingua portuguesa.

* Engenharia de Prompts e Guardrails: O system prompt do agente instrui o Claude a responder exclusivamente com base nos trechos fornecidos do relatorio, nunca emitir diagnosticos medicos definitivos, nunca prescrever medicamentos ou dosagens, utilizar uma linguagem empatica e acessivel, e incluir obrigatoriamente a recomendacao de consulta medica para decisoes clinicas.

---

## Telas do Sistema

* Upload: Pagina inicial com area de drag-and-drop com feedback visual do processamento em tempo real.
* Dashboard de Riscos: Cards interativos organizados por nivel de criticidade (Alto, Medio, Baixo), resumo executivo e modais detalhados com recomendacoes especificas.
* Chatbot: Interface limpa de conversacao contendo sugestoes de perguntas frequentes baseadas no arquivo e um disclaimer medico fixo no rodape.

---

## Estrutura do Projeto

```text
genai-genera/
├── backend/
│   ├── main.py                 # API FastAPI — Endpoints principais
│   ├── pdf_extractor.py        # Extracao de texto bruto do PDF
│   ├── json_structurer.py      # Claude estruturando a massa de dados em JSON
│   ├── embedding_service.py    # Integracao com Voyage AI e transferencia
│   ├── rag_service.py          # Mecanismo de busca semantica e orquestracao do LLM
│   ├── requirements.txt        # Dependencias Python
│   └── .env.example            # Modelo de variaveis de ambiente do backend
└── frontend/
    ├── app/
    │   ├── page.tsx            # Tela de upload (Home)
    │   ├── dashboard/
    │   │   └── page.tsx        # Dashboard visual de riscos
    │   └── chat/
    │       └── page.tsx        # Interface do Chatbot
    └── lib/
        └── api.ts              # Cliente de consumo da API FastAPI
