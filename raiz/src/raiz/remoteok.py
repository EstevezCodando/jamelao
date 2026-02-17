from __future__ import annotations

import http.client
import json
import shutil
from pathlib import Path
from typing import Iterable, Iterator

from bs4 import BeautifulSoup


def baixar_para_arquivo(*, server_name: str, url: str, expected_status: int, filename: str) -> None:
    caminho = Path(filename)
    if caminho.is_file():
        return

    conn = http.client.HTTPSConnection(server_name)
    try:
        conn.request("GET", url)
        response = conn.getresponse()
        if expected_status != response.status:
            raise RuntimeError(
                f"Status inesperado {response.status} ao requisitar GET {server_name}{url}"
            )
        with open(caminho, "wb") as arquivo:
            shutil.copyfileobj(response, arquivo)
    finally:
        conn.close()


def extrair_jsonld(sopa: BeautifulSoup) -> Iterator[dict]:
    for el in sopa.select("script[type='application/ld+json']"):
        yield json.loads(el.text)


def extrair_jobs_minimos_de_jsonld(itens_jsonld: Iterable[dict]) -> Iterator[dict]:
    for v in itens_jsonld:
        yield {
            "title": v["title"],
            "company": v["hiringOrganization"]["name"],
            "link": v["hiringOrganization"]["sameAs"],
            "description": v["description"],
        }


def escrever_jsonl_se_nao_existir(*, caminho_jsonl: str, registros: Iterable[dict]) -> None:
    caminho = Path(caminho_jsonl)
    if caminho.is_file():
        return

    with open(caminho, "w", encoding="utf-8", newline="\n") as saida:
        for r in registros:
            saida.write(json.dumps(r, ensure_ascii=False))
            saida.write("\n")
