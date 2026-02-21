import unittest

from bs4 import BeautifulSoup

from raiz.remoteok import extrair, extrair_jsonld, extrair_jobs_minimos_de_jsonld

HTML_COM_JOB = """
<html><body>
  <script type="application/ld+json">
    {
      "title": "Senior Engineer",
      "description": "Descrição do cargo",
      "hiringOrganization": {
        "name": "ACME",
        "sameAs": "https://acme.com"
      }
    }
  </script>
</body></html>
"""


class TestExtrairJobsMinimos(unittest.TestCase):
    def test_html_sem_jsonld_retorna_vazio(self) -> None:
        sopa = BeautifulSoup("<div></div>", "html.parser")
        self.assertEqual(list(extrair_jobs_minimos_de_jsonld(extrair_jsonld(sopa))), [])

    def test_extrai_quatro_campos_do_jsonld(self) -> None:
        sopa = BeautifulSoup(HTML_COM_JOB, "html.parser")
        itens = list(extrair_jobs_minimos_de_jsonld(extrair_jsonld(sopa)))

        self.assertEqual(len(itens), 1)
        self.assertEqual(itens[0]["title"],       "Senior Engineer")
        self.assertEqual(itens[0]["company"],     "ACME")
        self.assertEqual(itens[0]["link"],        "https://acme.com")
        self.assertEqual(itens[0]["description"], "Descrição do cargo")

    def test_extrair_e_atalho_para_pipeline_completo(self) -> None:
        sopa = BeautifulSoup(HTML_COM_JOB, "html.parser")
        itens = list(extrair(sopa))
        self.assertEqual(len(itens), 1)
        self.assertEqual(itens[0]["title"], "Senior Engineer")


if __name__ == "__main__":
    unittest.main()
