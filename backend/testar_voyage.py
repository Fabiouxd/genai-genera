import voyageai
from dotenv import load_dotenv
import os

load_dotenv()

client = voyageai.Client(api_key=os.getenv("VOYAGE_API_KEY"))

resposta = client.embed(
    ["Teste de embedding do projeto GenAI Genera"],
    model="voyage-3-lite",
    input_type="document"
)

print(f"Funcionou! Tamanho do vetor: {len(resposta.embeddings[0])}")