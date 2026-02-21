import json
from typing import Iterable, Iterator

from bs4 import BeautifulSoup


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


def extrair(sopa: BeautifulSoup) -> Iterator[dict]:
    """Ponto de entrada para o core: recebe sopa, devolve registros."""
    return extrair_jobs_minimos_de_jsonld(extrair_jsonld(sopa))
