from pathlib import Path

from bs4 import BeautifulSoup

from raiz.chave import chave_deterministica
from raiz.provedores import PROVEDORES
from raiz.remoteok import (
    baixar_para_arquivo,
    escrever_jsonl_se_nao_existir,
    extrair_jobs_minimos_de_jsonld,
    extrair_jsonld,
)


def main() -> None:
    provedor = PROVEDORES["remoteok"]
    chave = chave_deterministica(provedor=provedor.nome, url_absoluta=provedor.url_absoluta)

    pasta_saida = Path("data") / "raw" / provedor.nome / chave
    pasta_saida.mkdir(parents=True, exist_ok=True)

    caminho_html = pasta_saida / "captura.html"
    caminho_jsonl = pasta_saida / "extracao.jsonl"

    baixar_para_arquivo(
        host=provedor.host,
        caminho=provedor.caminho,
        expected_status=200,
        destino=str(caminho_html),
    )

    with open(caminho_html, encoding="utf-8") as arquivo:
        sopa = BeautifulSoup(arquivo, "html.parser")

    registros = extrair_jobs_minimos_de_jsonld(extrair_jsonld(sopa))
    escrever_jsonl_se_nao_existir(destino=str(caminho_jsonl), registros=registros)


if __name__ == "__main__":
    main()
