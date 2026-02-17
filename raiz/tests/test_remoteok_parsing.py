import unittest

from bs4 import BeautifulSoup

from raiz.remoteok import extrair_jsonld, extrair_jobs_minimos_de_jsonld


class TestRemoteOkParsing(unittest.TestCase):
    def test_extrai_quatro_campos_do_jsonld(self):
        html = """
        <html><head></head><body>
          <script type="application/ld+json">
            {
              "title": "Senior Engineer",
              "description": "Desc",
              "hiringOrganization": {
                "name": "ACME",
                "sameAs": "https://example.com"
              }
            }
          </script>
        </body></html>
        """
        sopa = BeautifulSoup(html, "html.parser")
        itens = list(extrair_jobs_minimos_de_jsonld(extrair_jsonld(sopa)))

        self.assertEqual(len(itens), 1)
        self.assertEqual(itens[0]["title"], "Senior Engineer")
        self.assertEqual(itens[0]["company"], "ACME")
        self.assertEqual(itens[0]["link"], "https://example.com")
        self.assertEqual(itens[0]["description"], "Desc")
