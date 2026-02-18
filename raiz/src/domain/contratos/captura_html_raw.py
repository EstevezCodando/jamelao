import hashlib


def chave_deterministica(*, url, server_name):
    """
    Cria um nome unico de 64 caracteres para uma combinacao de nome + URL
    """
    return hashlib.sha256(f"{url}|{server_name}".encode("utf-8")).hexdigest()
