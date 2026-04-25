import pdfplumber
import os

def extrair_texto_pdf(caminho_arquivo: str) -> dict:
    """
    Recebe o caminho de um arquivo PDF e retorna
    o texto extraído página por página.
    """
    
    texto_completo = ""
    total_paginas = 0
    
    try:
        with pdfplumber.open(caminho_arquivo) as pdf:
            total_paginas = len(pdf.pages)
            
            for numero, pagina in enumerate(pdf.pages):
                texto_pagina = pagina.extract_text()
                
                # Algumas páginas podem ser imagens — ignora se vazio
                if texto_pagina:
                    texto_completo += f"\n=== PÁGINA {numero + 1} ===\n"
                    texto_completo += texto_pagina
        
        return {
            "sucesso": True,
            "total_paginas": total_paginas,
            "texto": texto_completo,
            "tamanho_caracteres": len(texto_completo)
        }
    
    except Exception as erro:
        return {
            "sucesso": False,
            "erro": str(erro),
            "texto": ""
        }


# Teste rápido — rode este arquivo diretamente para testar
if __name__ == "__main__":
    # Coloque o caminho de qualquer PDF que você tenha para testar
    
    caminho_teste = "teste.pdf"
    
    if os.path.exists(caminho_teste):
        resultado = extrair_texto_pdf(caminho_teste)
        
        if resultado["sucesso"]:
            print(f"Páginas extraídas: {resultado['total_paginas']}")
            print(f"Total de caracteres: {resultado['tamanho_caracteres']}")
            print("\nPrimeiros 500 caracteres:")
            print(resultado["texto"][:500])
        else:
            print(f"Erro: {resultado['erro']}")
    else:
        print("Coloque um arquivo chamado teste.pdf na pasta backend/ para testar")