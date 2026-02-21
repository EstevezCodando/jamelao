import http.client
import json
import shutil
from pathlib import Path
from typing import Iterable

from bs4 import BeautifulSoup

from raiz.chave import chave_deterministica
from raiz.provedores import Provedor


def baixar_para_arquivo(*, host: str, caminho: str, expected_status: int, destino: Path) -> None:
    if destino.is_file():
        return

    conn = http.client.HTTPSConnection(host)
    try:
        conn.request("GET", caminho)
        resposta = conn.getresponse()
        if resposta.status != expected_status:
            raise RuntimeError(f"Status inesperado {resposta.status} em GET {host}{caminho}")
        with open(destino, "wb") as saida:
            shutil.copyfileobj(resposta, saida)
    finally:
        conn.close()


def escrever_jsonl_se_nao_existir(*, destino: Path, registros: Iterable[dict]) -> None:

    if destino.is_file():
        return

    with open(destino, "w", encoding="utf-8", newline="\n") as saida:
        for r in registros:
            saida.write(json.dumps(r, ensure_ascii=False) + "\n")


def capturar(provedor: Provedor, pasta_raiz: Path) -> None:
    chave = chave_deterministica(provedor=provedor.nome, url_absoluta=provedor.url_absoluta)

    pasta = pasta_raiz / provedor.nome / chave
    pasta.mkdir(parents=True, exist_ok=True)

    caminho_html = pasta / "captura.html"
    caminho_jsonl = pasta / "extracao.jsonl"

    baixar_para_arquivo(
        host=provedor.host,
        caminho=provedor.caminho,
        expected_status=200,
        destino=caminho_html,
    )

    with open(caminho_html, encoding="utf-8") as arquivo:
        sopa = BeautifulSoup(arquivo, "html.parser")

    escrever_jsonl_se_nao_existir(
        destino=caminho_jsonl,
        registros=provedor.extrair(sopa),
    )
