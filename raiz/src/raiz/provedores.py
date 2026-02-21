from dataclasses import dataclass
from typing import Callable, Iterator

from bs4 import BeautifulSoup

from raiz.remoteok import extrair as extrair_remoteok


@dataclass(frozen=True, slots=True)
class Provedor:
    nome: str
    host: str
    proxima_pagina: Callable[[int], str]
    extrair: Callable[[BeautifulSoup], Iterator[dict]]

    @property
    def url_absoluta(self) -> str:
        return f"https://{self.host}{self.proxima_pagina(0)}"


PROVEDORES: dict[str, Provedor] = {
    "remoteok": Provedor(
        nome="remoteok",
        host="remoteok.com",
        proxima_pagina=lambda p: f"/?tags=software&action=get_jobs&premium=0&pagination=1&offset={p * 10}",
        extrair=extrair_remoteok,
    ),
}