🧬 GenAI Genera
Transformando relatórios genéticos em conversas inteligentes

Projeto acadêmico desenvolvido para o Challenge Dasa + Genera — FIAP 2026


O Problema
Você já recebeu um resultado de exame e não entendeu nada?
Agora imagina receber um relatório genético de 40 páginas com frases como:
"Polimorfismo rs429358 no gene APOE — alelo ε4 detectado."
É exatamente isso que acontece com milhares de pacientes da Genera (Dasa) todos os anos. O relatório chega, vai para a gaveta, e nenhuma mudança de hábito acontece — porque ninguém conseguiu entender o que estava escrito.
Esse é o problema que o GenAI Genera resolve.

A Solução
O GenAI Genera transforma qualquer relatório genético em PDF em uma conversa inteligente. O paciente faz o upload do seu relatório e em minutos pode:

📋 Ver um resumo em linguagem humana do que o relatório diz
🎯 Visualizar seus principais riscos organizados por prioridade
💬 Conversar com uma IA que conhece o seu relatório específico
🏃 Receber recomendações práticas para o dia a dia

Sem jargão médico. Sem ansiedade desnecessária. Com informação de verdade.

Como Funciona
📄 PDF Upload
     ↓
📝 Extração de texto (pdfplumber)
     ↓
🧠 Estruturação em JSON (Claude AI)
     ↓
🔢 Geração de Embeddings (Voyage AI)
     ↓
🗄️ Armazenamento vetorial (Supabase + pgvector)
     ↓
💬 Usuário faz uma pergunta
     ↓
🔍 Busca semântica nos chunks do relatório
     ↓
✨ Claude responde com contexto real do relatório
     ↓
🖥️ Resposta aparece no chatbot (Next.js)

Stack de Tecnologias
CamadaTecnologiaPor quê?BackendPython + FastAPIEcossistema mais rico para IA/MLExtração de PDFpdfplumberPreserva estrutura de texto e tabelasIA / LLMClaude Haiku (Anthropic)Precisão em textos médicos, custo acessívelEmbeddingsVoyage AI (voyage-3-lite)Parceiro oficial da Anthropic, gratuitoBanco de dadosSupabase + pgvectorVetores e SQL no mesmo lugar, sem servidorFrontendNext.js 14 + Tailwind CSSPerformance, deploy fácil, visual moderno

Telas do Sistema
Upload
Tela inicial com área de drag-and-drop. Arraste seu PDF e aguarde o processamento.
O sistema extrai o texto, analisa com IA e gera os embeddings automaticamente.
Dashboard
Cards coloridos organizados por nível de risco:

🔴 Risco Alto — requer atenção imediata
🟡 Risco Médio — monitorar e agir
🟢 Risco Baixo — manter acompanhamento

Clique em qualquer card para ver detalhes e recomendações específicas.
Chatbot
Interface de chat com a IA. Perguntas sugeridas para quem não sabe por onde começar.
A IA responde baseada exclusivamente no seu relatório — sem respostas genéricas.

Como Rodar Localmente
Pré-requisitos

Python 3.11+
Node.js 18+
Conta no Supabase (gratuito)
Chave de API da Anthropic
Chave de API do Voyage AI

Backend
bashcd backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux
pip install -r requirements.txt
cp .env.example .env         # Preencha com suas chaves
uvicorn main:app --reload
API rodando em: http://localhost:8000
Documentação interativa: http://localhost:8000/docs
Banco de Dados (Supabase)
No SQL Editor do Supabase, execute o script em /backend/setup_banco.sql para criar as tabelas e a função de busca semântica.
Frontend
bashcd frontend
npm install
npm run dev
Acesse: http://localhost:3000

Estrutura do Projeto
genai-genera/
├── backend/
│   ├── main.py                 # API FastAPI — endpoints principais
│   ├── pdf_extractor.py        # Extração de texto do PDF
│   ├── json_structurer.py      # Claude estrutura os dados em JSON
│   ├── embedding_service.py    # Voyage AI gera e salva embeddings
│   ├── rag_service.py          # Busca semântica + resposta com RAG
│   ├── requirements.txt        # Dependências Python
│   └── .env.example            # Modelo de variáveis de ambiente
└── frontend/
    ├── app/
    │   ├── page.tsx            # Tela de upload
    │   ├── dashboard/
    │   │   └── page.tsx        # Dashboard de riscos
    │   └── chat/
    │       └── page.tsx        # Chatbot
    └── lib/
        └── api.ts              # Funções para consumir a API

Exemplo de JSON Gerado
Após o processamento do PDF, o sistema gera um JSON estruturado assim:
json{
  "paciente": {
    "nome": "João Silva",
    "data_exame": "2024-11-20"
  },
  "predisposicoes": [
    {
      "condicao": "Dislipidemia e Risco Cardiovascular",
      "risco": "medio",
      "gene": "APOE",
      "variante": "ε4",
      "explicacao_simples": "Seus níveis de colesterol LDL e triglicérides estão elevados. Isso aumenta o risco de problemas no coração e vasos sanguíneos.",
      "recomendacao": "Reduzir gorduras saturadas, praticar exercícios e consultar um cardiologista."
    }
  ],
  "recomendacoes_gerais": [
    "Consultar cardiologista para avaliação completa",
    "Repetir exames de colesterol em 3 meses",
    "Praticar 150 minutos de exercício por semana"
  ],
  "resumo_executivo": "Relatório com 3 pontos de atenção principais..."
}

Segurança e LGPD
Dados genéticos são classificados como dados sensíveis pelo Art. 5º da LGPD.
O GenAI Genera trata isso com seriedade:

🔐 Comunicação criptografada via HTTPS
🎭 PDFs deletados do servidor após o processamento
⏰ Dados retidos por 90 dias com opção de exclusão
📝 Consentimento explícito solicitado antes do upload
🚫 Dados nunca usados para treinar modelos


Disclaimer: As informações geradas têm caráter educativo e não substituem consulta com médico ou profissional de saúde qualificado.


A Jornada de Desenvolvimento
Construir esse projeto não foi um caminho reto. Houve alguns obstáculos que vale registrar:
APIs gratuitas e seus limites: Tentamos usar Gemini e OpenAI nos planos gratuitos — ambos retornaram cota zerada. No final, optamos pela Anthropic para a IA principal e Voyage AI para embeddings, que funcionou perfeitamente.
Rate limiting do Voyage AI: Sem cartão cadastrado, o plano gratuito limita a 3 requisições por minuto. Resolvemos com um time.sleep(20) entre os chunks — não elegante, mas funcional para desenvolvimento.
pgvector e dimensões: Trocamos de API de embeddings três vezes durante o desenvolvimento (OpenAI → Gemini → Voyage AI), e cada uma tem dimensões diferentes (1536, 768, 512). Cada troca exigiu recriar a tabela no banco. Lição aprendida: definir a stack de embeddings antes de começar.
RLS do Supabase: O Row Level Security bloqueia inserções por padrão. Custou alguns minutos de depuração até entender que era uma questão de permissão, não de código.
Cada um desses problemas virou aprendizado real sobre como sistemas de IA funcionam em produção.

Próximos Passos

 Autenticação de usuários com histórico de relatórios
 Suporte a múltiplos PDFs por paciente
 Modo médico com visão técnica avançada
 Deploy em produção (Vercel + Railway)
 Integração com prontuário eletrônico (padrão FHIR)
 App mobile (React Native)
 Suporte a relatórios de outros laboratórios


Time
FABIO MENDES, BERNANRDO RUPOLO, MARCOS VINICIUS DOS SANTOS MORGADO, LEONARDO MAGALHAES