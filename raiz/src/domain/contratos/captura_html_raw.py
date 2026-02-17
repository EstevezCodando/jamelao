from __future__ import annotations

import hashlib
from typing import Annotated

from pydantic import AnyHttpUrl, BaseModel, Field

Sha256Hex = Annotated[
    str, Field(min_length=64, max_length=64, pattern=r"^[0-9a-f]{64}$")
]


class CapturaHtmlRawRequest(BaseModel):
    url: AnyHttpUrl
    source: str = Field(default="remoteok", min_length=1)

    def chave_deterministica(self) -> Sha256Hex:
        base = f"{str(self.url)}|{self.source}".encode("utf-8")
        return hashlib.sha256(base).hexdigest()
