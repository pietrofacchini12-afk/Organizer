import os
import sys
import time
import shutil
from pathlib import Path
from datetime import datetime


pasta_downloads = Path.home() / "Downloads"

pasta_destino = pasta_downloads

intervalo_segundos = 2

extensoes_temporarias = {".crdownload", ".part", ".tmp", ".download", ".opdownload"}


regras = [
    {
        "pasta": "Escola",
        "descricao": "Provas, trabalhos e materiais da escola",
        "palavras_chave": [
            "Escola", "prova", "tarefa", "estudo", "provas",
            "teste", "testes", "exercicio", "exercício",
            "exercicios", "exercícios", "escola", "school"
        ],
        "extensoes": []
    },
    {
        "pasta": "Arquivos do Cura",
        "descricao": "Arquivos fatiados no Cura",
        "palavras_chave": ["cura", "ultimaker"],
        "extensoes": [".gcode", ".ufp"]
    },
    {
        "pasta": "Modelos 3D",
        "descricao": "Modelos para impressão 3D",
        "palavras_chave": ["stl", "3dprint", "modelo 3d", "3d model"],
        "extensoes": [".stl", ".obj", ".3mf", ".step", ".stp"]
    },
    {
        "pasta": "Jogos",
        "descricao": "Jogos e ROMs",
        "palavras_chave": ["game", "jogo", "repack", "steam", "rom", "emulator", "emulador", "mod"],
        "extensoes": [
            ".iso", ".rom", ".nes", ".sfc", ".gba", ".nds",
            ".3ds", ".xapk", ".nsp", ".xci", ".wbfs", ".cso"
        ]
    },
    {
        "pasta": "Documentos",
        "descricao": "Documentos em geral",
        "palavras_chave": [],
        "extensoes": [
            ".pdf", ".docx", ".doc", ".txt", ".xlsx", ".xls",
            ".pptx", ".ppt", ".csv", ".odt", ".rtf", ".epub"
        ]
    },
    {
        "pasta": "Imagens",
        "descricao": "Fotos e designs",
        "palavras_chave": [],
        "extensoes": [
            ".jpg", ".jpeg", ".png", ".gif", ".webp",
            ".svg", ".bmp", ".ico", ".psd", ".ai"
        ]
    },
    {
        "pasta": "Vídeos",
        "descricao": "Filmes e gravações",
        "palavras_chave": [],
        "extensoes": [
            ".mp4", ".mkv", ".avi", ".mov", ".wmv", ".webm", ".flv"
        ]
    },
    {
        "pasta": "Músicas",
        "descricao": "Áudios e músicas",
        "palavras_chave": [],
        "extensoes": [
            ".mp3", ".wav", ".flac", ".ogg", ".m4a", ".aac"
        ]
    },
    {
        "pasta": "Compactados",
        "descricao": "Arquivos compactados",
        "palavras_chave": [],
        "extensoes": [
            ".zip", ".rar", ".7z", ".tar", ".gz"
        ]
    },
    {
        "pasta": "Programas",
        "descricao": "Instaladores e programas",
        "palavras_chave": [],
        "extensoes": [
            ".exe", ".msi", ".bat"
        ]
    }
]


pasta_outros = "Outros"



def log(mensagem: str, tipo: str = "INFO"):
    hora = datetime.now().strftime("%H:%M:%S")
    print(f"[{hora}] [{tipo}] {mensagem}")


def arquivo_terminou_de_baixar(caminho_arquivo: Path) -> bool:

    if not caminho_arquivo.exists():
        return False

    if caminho_arquivo.suffix.lower() in extensoes_temporarias:
        return False

    try:

        tam1 = caminho_arquivo.stat().st_size
        time.sleep(0.4)
        tam2 = caminho_arquivo.stat().st_size
        if tam1 != tam2:
            return False

        with open(caminho_arquivo, "r+b"):
            pass
        return True
    except (PermissionError, OSError):
        return False


def obter_pasta_destino(caminho_arquivo: Path) -> str:

    nome_lower = caminho_arquivo.name.lower()
    extensao_lower = caminho_arquivo.suffix.lower()


    for regra in regras:
        for palavra in regra["palavras_chave"]:
            if palavra.lower() in nome_lower:
                return regra["pasta"]


    for regra in regras:
        extensoes_regra = [e.lower() for e in regra["extensoes"]]
        if extensao_lower in extensoes_regra:
            return regra["pasta"]

    return pasta_outros


def gerar_caminho_sem_sobrescrever(pasta_destino: Path, nome_arquivo: str) -> Path:

    alvo = pasta_destino / nome_arquivo
    if not alvo.exists():
        return alvo

    nome_base = alvo.stem
    extensao = alvo.suffix
    contador = 1

    while True:
        novo_candidato = pasta_destino / f"{nome_base} ({contador}){extensao}"
        if not novo_candidato.exists():
            return novo_candidato
        contador += 1


def processar_arquivo(caminho_arquivo: Path):

    if not caminho_arquivo.is_file():
        return


    if caminho_arquivo.name == Path(__file__).name:
        return


    if not arquivo_terminou_de_baixar(caminho_arquivo):
        return

    pasta_nome = obter_pasta_destino(caminho_arquivo)
    if not pasta_nome:
        return

    destino = pasta_destino / pasta_nome
    destino.mkdir(parents=True, exist_ok=True)

    novo_caminho = gerar_caminho_sem_sobrescrever(destino, caminho_arquivo.name)

    try:
        shutil.move(str(caminho_arquivo), str(novo_caminho))
        log(f'"{caminho_arquivo.name}" -> [{pasta_nome}]', tipo="OK")
    except Exception as erro:
        log(f'Erro ao mover "{caminho_arquivo.name}": {erro}', tipo="ERRO")


def varrer_pasta():

    try:
        for item in pasta_downloads.iterdir():
            if item.is_file():
                processar_arquivo(item)
    except Exception as e:
        log(f"Erro ao ler pasta: {e}", tipo="ERRO")


def main():
    print(f"Organizador de downloads rodando em: {pasta_downloads}")
    print("Regras ativas:")
    print("  - Provas / Estudos      -> Pasta 'Escola'")
    print("  - Arquivos .STL         -> Pasta 'Modelos 3D'")
    print("  - Arquivos .GCODE/Cura  -> Pasta 'Arquivos do Cura'")
    print("  - Jogos / ISOs / ROMs   -> Pasta 'Jogos'")
    print("Pressione Ctrl + C para encerrar a qualquer momento.\n")

    log("Organizando arquivos já existentes...")
    varrer_pasta()
    log("Aguardando novos downloads...")

    try:
        while True:
            time.sleep(intervalo_segundos)
            varrer_pasta()
    except KeyboardInterrupt:
        print("\nFinalizado. Até mais!")


if __name__ == "__main__":
    main()
