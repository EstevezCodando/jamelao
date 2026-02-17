from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from typing import Literal

from pydantic import AnyHttpUrl, BaseModel, Field


PIPELINE_VERSION_PADRAO = "raiz.captura_html_raw.v1"


class CapturaHtmlRawRequest(BaseModel):

    pipeline_version: str = Field(default=PIPELINE_VERSION_PADRAO, min_length=1)
    url: AnyHttpUrl
    source: str = Field(default="remoteok", min_length=1)

    user_agent: str | None = Field(default=None, max_length=300)

    usar_apify_proxy: bool = False
    apify_proxy_groups: list[str] | None = None
    apify_proxy_country_code: str | None = Field(default=None, max_length=2)
    apify_proxy_session: str | None = Field(default=None, max_length=50)

    socks_proxy_url: str | None = Field(
        default=None,
        description="Ex.: socks5://127.0.0.1:9050 (opcional).",
        max_length=300,
    )

    timeout_s: float = Field(default=30.0, ge=1.0, le=120.0)

    def chave_deterministica(self) -> str:
        """Chave determinística para idempotência.

        """

        grupos = ",".join(self.apify_proxy_groups or [])

        partes = [
            self.pipeline_version,
            str(self.url),
            self.source,
            (self.user_agent or "").strip(),
            "apify" if self.usar_apify_proxy else "",
            grupos.strip(),
            (self.apify_proxy_country_code or "").strip(),
            (self.apify_proxy_session or "").strip(),
            (self.socks_proxy_url or "").strip(),
        ]

        base = "|".join(partes).encode("utf-8")
        return hashlib.sha256(base).hexdigest()



class CapturaHtmlRawResponse(BaseModel):

    pipeline_version: str
    run_id: str
    chave_deterministica: str

    source: str
    url: AnyHttpUrl

    status: Literal["OK", "ERRO"]
    http_status_code: int | None = None
    erro_categoria: str | None = None
    erro_mensagem: str | None = None

    armazenado_em: str | None = None
    metadata_em: str | None = None

    html_sha256: str | None = None
    tamanho_bytes: int | None = None
    capturado_em_utc: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    titulo_detectado: str | None = None
