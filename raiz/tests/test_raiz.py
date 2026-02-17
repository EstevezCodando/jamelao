import unittest

from bs4 import BeautifulSoup

from raiz.remoteok import extrair_jsonld, extrair_jobs_minimos_de_jsonld


class TestExtrairJobsMinimos(unittest.TestCase):
    def test_html_sem_jsonld_retorna_vazio(self) -> None:
        sopa = BeautifulSoup("<div></div>", "html.parser")
        resultado = list(extrair_jobs_minimos_de_jsonld(extrair_jsonld(sopa)))
        self.assertEqual(resultado, [])


if __name__ == "__main__":
    unittest.main()
