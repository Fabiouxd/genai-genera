from supabase import create_client
from dotenv import load_dotenv
import os

# Carrega as variáveis do arquivo .env
load_dotenv()

# Conecta ao Supabase
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

# Tenta buscar os relatórios (vai retornar lista vazia, mas sem erro)
resultado = supabase.table("relatorios").select("*").execute()

print("Conexão bem-sucedida!")
print(f"Relatórios no banco: {len(resultado.data)}")