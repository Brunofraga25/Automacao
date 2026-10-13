
from pathlib import Path
import shutil

# 1. Localização da pasta Downloads
PASTA_DOWNLOADS = Path.home() / "Downloads"

# 2. Categorias e extensões dos arquivos
CATEGORIAS = {
    "Documentos": {
        ".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt",
        ".xls", ".xlsx", ".csv", ".ppt", ".pptx", ".ods", ".odp"
    },
    "Imagens": {
        ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp",
        ".svg", ".tif", ".tiff", ".ico"
    },
    "Videos": {
        ".mp4", ".mkv", ".avi", ".mov", ".wmv", ".webm", ".m4v"
    },
    "Audios": {
        ".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a", ".wma"
    },
    "Compactados": {
        ".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"
    },
    "Instaladores": {
        ".exe", ".msi", ".msix", ".appx"
    },
    "Codigo": {
        ".py", ".js", ".html", ".css", ".java", ".c", ".cpp",
        ".json", ".xml", ".sql", ".php", ".ts", ".jsx", ".tsx"
    }
}


# 3. Identifica a categoria de um arquivo
def identificar_categoria(arquivo):
    extensao = arquivo.suffix.lower()

    for categoria, extensoes in CATEGORIAS.items():
        if extensao in extensoes:
            return categoria

    return "Outros"


# 4. Converte bytes para uma unidade mais fácil de ler
def formatar_tamanho(bytes_):
    tamanho_mb = bytes_ / (1024 * 1024)

    if tamanho_mb >= 1024:
        return f"{tamanho_mb / 1024:.2f} GB"

    return f"{tamanho_mb:.2f} MB"


# 5. Retorna os arquivos diretamente na pasta Downloads
def listar_arquivos():
    return [
        item for item in PASTA_DOWNLOADS.iterdir()
        if item.is_file()
    ]


# 6. Lista os arquivos encontrados
def mostrar_arquivos():
    arquivos = listar_arquivos()

    if not arquivos:
        print("\nNenhum arquivo encontrado na raiz de Downloads.")
        return

    print("\n--- Arquivos em Downloads ---")

    for arquivo in arquivos:
        try:
            tamanho = arquivo.stat().st_size
            print(f"{arquivo.name} | {formatar_tamanho(tamanho)}")
        except OSError:
            print(f"{arquivo.name} | Não foi possível ler o tamanho")


# 7. Evita sobrescrever arquivos com o mesmo nome
def escolher_destino_unico(pasta_destino, nome_arquivo):
    destino = pasta_destino / nome_arquivo

    if not destino.exists():
        return destino

    nome = Path(nome_arquivo).stem
    extensao = Path(nome_arquivo).suffix
    contador = 1

    while True:
        novo_nome = f"{nome} ({contador}){extensao}"
        destino = pasta_destino / novo_nome

        if not destino.exists():
            return destino

        contador += 1


# 8. Organiza os arquivos por categoria
def organizar_arquivos():
    arquivos = listar_arquivos()

    if not arquivos:
        print("\nNão há arquivos para organizar.")
        return

    # Prepara a lista de operações sem mover nada ainda
    operacoes = []

    for arquivo in arquivos:
        categoria = identificar_categoria(arquivo)
        pasta_destino = PASTA_DOWNLOADS / categoria

        operacoes.append((arquivo, pasta_destino, categoria))

    print("\n--- Prévia da organização ---")

    for arquivo, pasta_destino, categoria in operacoes:
        print(f"{arquivo.name} -> {categoria}/")

    print(f"\nTotal de arquivos: {len(operacoes)}")
    confirmacao = input(
        "\nDeseja mover esses arquivos? Digite S para confirmar: "
    ).strip().lower()

    if confirmacao != "s":
        print("\nOperação cancelada. Nenhum arquivo foi movido.")
        return

    movidos = 0
    falhas = 0

    for arquivo, pasta_destino, categoria in operacoes:
        try:
            # Cria a pasta da categoria se necessário
            pasta_destino.mkdir(parents=True, exist_ok=True)

            # Escolhe um nome que não sobrescreva outro arquivo
            destino = escolher_destino_unico(
                pasta_destino, arquivo.name
            )

            # Move o arquivo
            shutil.move(str(arquivo), str(destino))

            print(f"Movido: {arquivo.name} -> {categoria}/")
            movidos += 1

        except OSError as erro:
            print(f"Erro ao mover {arquivo.name}: {erro}")
            falhas += 1

    print("\n--- Resultado ---")
    print(f"Arquivos movidos: {movidos}")
    print(f"Falhas: {falhas}")


# 9. Busca arquivos por extensão
def buscar_por_extensao():
    extensao = input(
        "\nDigite a extensão (exemplo: pdf ou .pdf): "
    ).strip().lower()

    if not extensao:
        print("Nenhuma extensão informada.")
        return

    if not extensao.startswith("."):
        extensao = "." + extensao

    encontrados = [
        arquivo for arquivo in listar_arquivos()
        if arquivo.suffix.lower() == extensao
    ]

    print(f"\nArquivos encontrados com {extensao}: {len(encontrados)}")

    for arquivo in encontrados:
        print(arquivo.name)


# 10. Calcula o espaço ocupado pelos arquivos
def analisar_espaco():
    total_bytes = 0
    arquivos = listar_arquivos()

    for arquivo in arquivos:
        try:
            total_bytes += arquivo.stat().st_size
        except OSError:
            print(f"Não foi possível ler: {arquivo.name}")

    print(f"\nArquivos analisados: {len(arquivos)}")
    print(f"Espaço ocupado: {formatar_tamanho(total_bytes)}")


# 11. Exibe o menu principal
def mostrar_menu():
    print("\n" + "=" * 35)
    print("       LIMPADOR DE DOWNLOADS")
    print("=" * 35)
    print("1 - Listar arquivos")
    print("2 - Organizar arquivos")
    print("3 - Buscar por extensão")
    print("4 - Analisar espaço ocupado")
    print("5 - Sair")
    print("=" * 35)


# 12. Controla a execução do programa
def main():
    if not PASTA_DOWNLOADS.is_dir():
        print(f"Pasta não encontrada: {PASTA_DOWNLOADS}")
        return

    while True:
        mostrar_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            mostrar_arquivos()

        elif opcao == "2":
            organizar_arquivos()

        elif opcao == "3":
            buscar_por_extensao()

        elif opcao == "4":
            analisar_espaco()

        elif opcao == "5":
            print("\nPrograma encerrado.")
            break

        else:
            print("\nOpção inválida. Tente novamente.")


# 13. Inicia o programa quando executado diretamente
if __name__ == "__main__":
    main()
