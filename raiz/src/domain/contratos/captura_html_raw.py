from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from typing import Annotated, ClassVar, Literal

from pydantic import AnyHttpUrl, BaseModel, Field

Sha256Hex = Annotated[str, Field(min_length=64, max_length=64, pattern=r"^[0-9a-f]{64}$")]


class CapturaHtmlRawRequest(BaseModel):
    PIPELINE_VERSION_PADRAO: ClassVar[str] = "raiz.captura_html_raw.v1"

    pipeline_version: str = Field(default=PIPELINE_VERSION_PADRAO, min_length=1)
    url: AnyHttpUrl
    source: str = Field(default="remoteok", min_length=1)

    timeout_s: float = Field(default=30.0, ge=1.0, le=120.0)

    def chave_deterministica(self) -> Sha256Hex:
        partes = [
            self.pipeline_version.strip(),
            str(self.url).strip(),
            self.source.strip(),
        ]
        base = "|".join(partes).encode("utf-8")
        return hashlib.sha256(base).hexdigest()


class CapturaHtmlRawResponse(BaseModel):
    pipeline_version: str = Field(min_length=1)
    run_id: str = Field(min_length=1)
    chave_deterministica: Sha256Hex

    source: str = Field(min_length=1)
    url: AnyHttpUrl

    status: Literal["OK", "ERRO"]
    http_status_code: int | None = None
    erro_mensagem: str | None = None

    # Pode ser path local ou URL, dependendo da estratégia de storage.
    armazenado_em: str | None = None

    html_sha256: Sha256Hex | None = None
    tamanho_bytes: int | None = Field(default=None, ge=0)

    capturado_em_utc: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
