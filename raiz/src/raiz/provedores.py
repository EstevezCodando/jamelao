from dataclasses import dataclass
from typing import Callable, Iterator

from bs4 import BeautifulSoup

from raiz.remoteok import extrair as extrair_remoteok


@dataclass(frozen=True, slots=True)
class Provedor:
    nome: str
    host: str
    caminho: str  # path + query, sempre relativo, sempre iniciando com "/"
    extrair: Callable[[BeautifulSoup], Iterator[dict]]

    @property
    def url_absoluta(self) -> str:
        return f"https://{self.host}{self.caminho}"


PROVEDORES: dict[str, Provedor] = {
    "remoteok": Provedor(
        nome="remoteok",
        host="remoteok.com",
        caminho="/?tags=software&action=get_jobs&premium=0&pagination=1&offset=",
        extrair=extrair_remoteok,
    ),
}
