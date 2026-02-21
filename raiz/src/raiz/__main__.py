from pathlib import Path

from raiz.core import coletar
from raiz.provedores import PROVEDORES


def main() -> None:
    for provedor in PROVEDORES.values():
        coletar(provedor, pasta_raiz=Path("data") / "raw")


if __name__ == "__main__":
    main()
