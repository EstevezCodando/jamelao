import http.client
import json
import shutil
from pathlib import Path
from typing import Iterable, Iterator

from bs4 import BeautifulSoup


def baixar_para_arquivo(*, host: str, caminho: str, expected_status: int, destino: str) -> None:
    arquivo = Path(destino)
    if arquivo.is_file():
        return

    conn = http.client.HTTPSConnection(host)
    try:
        conn.request("GET", caminho)
        resposta = conn.getresponse()
        if resposta.status != expected_status:
            raise RuntimeError(f"Status inesperado {resposta.status} em GET {host}{caminho}")
        with open(arquivo, "wb") as saida:
            shutil.copyfileobj(resposta, saida)
    finally:
        conn.close()


def extrair_jsonld(sopa: BeautifulSoup) -> Iterator[dict]:
    for el in sopa.select("script[type='application/ld+json']"):
        yield json.loads(el.text)


def extrair_jobs_minimos_de_jsonld(itens: Iterable[dict]) -> Iterator[dict]:
    for v in itens:
        yield {
            "title": v["title"],
            "company": v["hiringOrganization"]["name"],
            "link": v["hiringOrganization"]["sameAs"],
            "description": v["description"],
        }


def escrever_jsonl_se_nao_existir(*, destino: str, registros: Iterable[dict]) -> None:
    arquivo = Path(destino)
    if arquivo.is_file():
        return

    with open(arquivo, "w", encoding="utf-8", newline="\n") as saida:
        for r in registros:
            saida.write(json.dumps(r, ensure_ascii=False) + "\n")
