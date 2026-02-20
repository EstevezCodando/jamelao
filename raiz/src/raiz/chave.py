import hashlib


def chave_deterministica(*, provedor: str, url_absoluta: str) -> str:
    """Hash SHA-256 de 64 caracteres para a combinação de provedor + URL absoluta."""
    return hashlib.sha256(f"{url_absoluta}|{provedor}".encode()).hexdigest()
