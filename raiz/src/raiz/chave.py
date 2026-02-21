import hashlib


def chave_deterministica(*, provedor: str, url_absoluta: str) -> str:
    return hashlib.sha256(f"{url_absoluta}|{provedor}".encode()).hexdigest()
