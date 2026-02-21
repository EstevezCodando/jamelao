from dataclasses import dataclass
from typing import Callable, Iterator

from bs4 import BeautifulSoup


@dataclass(frozen=True, slots=True)
class Provedor:
    nome: str
    host: str
    proxima_pagina: Callable[[int], str]
    extrair: Callable[[BeautifulSoup], Iterator[dict]]
