from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import tempfile
import os

from pdf_extractor import extrair_texto_pdf
from json_structurer import estruturar_relatorio
from embedding_service import salvar_relatorio_completo
from rag_service import responder_pergunta

app = FastAPI(
    title="GenAI — Intérprete de Relatórios Genéticos",
    description="API para processar relatórios Genera com IA",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {
        "status": "online",
        "projeto": "GenAI Genera",
        "versao": "1.0.0"
    }

@app.post("/upload-relatorio")
async def upload_relatorio(arquivo: UploadFile = File(...)):
    if not arquivo.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Apenas arquivos PDF são aceitos"
        )
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp:
        conteudo = await arquivo.read()
        temp.write(conteudo)
        caminho_temp = temp.name
    
    try:
        print("Extraindo texto do PDF...")
        extracao = extrair_texto_pdf(caminho_temp)
        
        if not extracao["sucesso"]:
            raise HTTPException(
                status_code=422,
                detail=f"Erro na extração: {extracao['erro']}"
            )
        
        print("Estruturando dados com IA...")
        estruturacao = estruturar_relatorio(extracao["texto"])
        
        if not estruturacao["sucesso"]:
            raise HTTPException(
                status_code=422,
                detail=f"Erro na estruturação: {estruturacao['erro']}"
            )
        
        print("Salvando no banco de dados...")
        relatorio_id = salvar_relatorio_completo(
            estruturacao["dados"],
            extracao["texto"]
        )
        
        return {
            "sucesso": True,
            "relatorio_id": relatorio_id,
            "dados": estruturacao["dados"],
            "mensagem": "Relatório processado com sucesso!"
        }
    
    finally:
        os.unlink(caminho_temp)


class PerguntaRequest(BaseModel):
    pergunta: str
    relatorio_id: str


@app.post("/chat")
def chat(request: PerguntaRequest):
    if not request.pergunta.strip():
        raise HTTPException(
            status_code=400,
            detail="A pergunta não pode estar vazia"
        )
    
    if not request.relatorio_id.strip():
        raise HTTPException(
            status_code=400,
            detail="O ID do relatório é obrigatório"
        )
    
    resultado = responder_pergunta(
        request.pergunta,
        request.relatorio_id
    )
    
    return {
        "sucesso": True,
        "pergunta": request.pergunta,
        "resposta": resultado["resposta"],
        "chunks_usados": resultado["chunks_usados"]
    }