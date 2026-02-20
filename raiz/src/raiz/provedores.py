from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Provedor:
    nome: str
    host: str
    caminho: str

    @property
    def url_absoluta(self) -> str:
        return f"https://{self.host}{self.caminho}"


PROVEDORES: dict[str, Provedor] = {
    "remoteok": Provedor(
        nome="remoteok",
        host="remoteok.com",
        caminho="/?tags=software&action=get_jobs&premium=0&pagination=1&offset=",
    ),
}
