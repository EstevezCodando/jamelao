"""Funções comuns que serão usadas por múltiplos provedores de dados."""

import http.client
import json
import pathlib
import shutil
from pathlib import Path
from typing import Iterable

import bs4

from raiz.chave import chave_deterministica
from raiz.provedores import Provedor


def baixar_para_arquivo(*, host: str, caminho: str, expected_status: int, destino: Path) -> None:
    """Baixa um recurso HTTP(S) para um arquivo local, se ainda não existir."""
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
    """Escreve JSONL no destino apenas se o arquivo ainda não existir."""
    if destino.is_file():
        return

    with open(destino, "w", encoding="utf-8", newline="\n") as saida:
        for r in registros:
            saida.write(json.dumps(r, ensure_ascii=False) + "\n")


def contar_linhas(caminho: Path) -> int:
    """Conta linhas não vazias de um arquivo."""
    with open(caminho, encoding="utf-8") as f:
        return sum(1 for linha in f if linha.strip())


def _processar_pagina(provedor: Provedor, pasta: Path, caminho: str) -> int:
    caminho_html = pasta / "captura.html"
    caminho_jsonl = pasta / "extracao.jsonl"

    baixar_para_arquivo(host=provedor.host, caminho=caminho, expected_status=200, destino=caminho_html)

    with open(caminho_html, encoding="utf-8") as arquivo:
        sopa = bs4.BeautifulSoup(arquivo, "html.parser")

    escrever_jsonl_se_nao_existir(destino=caminho_jsonl, registros=provedor.extrair(sopa))

    return contar_linhas(caminho_jsonl)


def coletar(provedor: Provedor, pasta_raiz: Path, limite_paginas: int = 5) -> None:
    """Coleta páginas de um provedor até não haver mais resultados."""

    for pagina in range(limite_paginas):
        caminho = provedor.proxima_pagina(pagina)
        chave = chave_deterministica(
            provedor=provedor.nome,
            url_absoluta=f"https://{provedor.host}{caminho}",
        )

        pasta = pasta_raiz / provedor.nome / chave
        pasta.mkdir(parents=True, exist_ok=True)

        if _processar_pagina(provedor, pasta, caminho) == 0:
            break


def fetch_to_file(*, server_name, request_method, url, expected_status, filename, query_string, headers):
    file_path = pathlib.Path(filename)
    if file_path.is_file():
        ## Already exists
        return

    conn = http.client.HTTPSConnection(server_name)
    try:
        conn.request(request_method, f"{url}?{query_string}", headers=headers)
        response = conn.getresponse()
        if not (expected_status == response.status):
            raise RuntimeError("Unexpected status code")
        with open(filename, 'wb') as file:
            shutil.copyfileobj(response, file)
    finally:
        conn.close()


def fetch_all(vs):
    for v in vs:
        base_dir = v["base_dir"]
        filename = pathlib.Path(base_dir, "index.html")
        base_dir.mkdir(parents=True, exist_ok=True)
        fetch_to_file(
            ## TODO: Paginacao
            **v["next_request"](dict(server_name=v["server_name"],
                                     request_method="GET",
                                     url="/",
                                     query_string="tags=software&action=get_jobs&premium=0&pagination=1&offset=",
                                     expected_status=200,
                                     filename=filename),
                                0)
        )
        if v["target_file"].is_file():
            return

        with (open(filename, 'r') as raw_htm,
              open(v["target_file"], "w") as target):
            for x in v["extract"](bs4.BeautifulSoup(raw_htm, 'html.parser')):
                target.write(json.dumps(x))
                target.write("\n")


def date_como_nome_de_pasta(now):
    return f"{now}".replace(" ", "T").replace(":", "-")[:16]
