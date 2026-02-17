from __future__ import annotations

from pathlib import Path

from bs4 import BeautifulSoup

from domain.contratos.captura_html_raw import CapturaHtmlRawRequest
from raiz.remoteok import (
    baixar_para_arquivo,
    escrever_jsonl_se_nao_existir,
    extrair_jobs_minimos_de_jsonld,
    extrair_jsonld,
)

REMOTEOK_SERVER = "remoteok.com"
REMOTEOK_PATH = "/?tags=software&action=get_jobs&premium=0&pagination=1&offset="


def main() -> None:
    req = CapturaHtmlRawRequest(
        url=f"https://{REMOTEOK_SERVER}{REMOTEOK_PATH}",
        source="remoteok",
    )

    pasta_saida = Path("data") / "raw" / req.source / req.chave_deterministica()
    pasta_saida.mkdir(parents=True, exist_ok=True)

    caminho_html = pasta_saida / "captura.html"
    caminho_jsonl = pasta_saida / "extracao.jsonl"

    baixar_para_arquivo(
        server_name=REMOTEOK_SERVER,
        url=REMOTEOK_PATH,
        expected_status=200,
        filename=str(caminho_html),
    )

    with open(caminho_html, "r", encoding="utf-8") as arquivo:
        sopa = BeautifulSoup(arquivo, "html.parser")

    registros = extrair_jobs_minimos_de_jsonld(extrair_jsonld(sopa))
    escrever_jsonl_se_nao_existir(caminho_jsonl=str(caminho_jsonl), registros=registros)


if __name__ == "__main__":
    main()
