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


def main() -> None:
    req = CapturaHtmlRawRequest(
        url="https://remoteok.com/?tags=software&action=get_jobs&premium=0&pagination=1&offset=",
        source="remoteok",
        user_agent=None,
        usar_apify_proxy=False,
        socks_proxy_url=None,
    )

    chave = req.chave_deterministica()

    pasta_saida = Path("data") / "raw" / req.source / chave
    pasta_saida.mkdir(parents=True, exist_ok=True)

    caminho_html = pasta_saida / "captura.html"
    caminho_jsonl = pasta_saida / "extracao.jsonl"

    baixar_para_arquivo(
        server_name="remoteok.com",
        request_method="GET",
        url="/?tags=software&action=get_jobs&premium=0&pagination=1&offset=",
        expected_status=200,
        filename=str(caminho_html),
    )

    with open(caminho_html, "r", encoding="utf-8") as arquivo:
        sopa = BeautifulSoup(arquivo, "html.parser")

    registros = extrair_jobs_minimos_de_jsonld(extrair_jsonld(sopa))
    escrever_jsonl_se_nao_existir(caminho_jsonl=str(caminho_jsonl), registros=registros)


if __name__ == "__main__":
    main()
