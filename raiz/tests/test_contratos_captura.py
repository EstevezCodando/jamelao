import unittest

from domain.contratos.captura_html_raw import CapturaHtmlRawRequest


class TestCapturaHtmlRawRequest(unittest.TestCase):
    def test_chave_deterministica_igual_para_mesma_entrada(self) -> None:
        req_a = CapturaHtmlRawRequest(
            url="https://remoteok.com/remote-jobs/remote-senior-full-stack-engineer-aguru-uk-1104983",
            source="remoteok",
        )
        req_b = CapturaHtmlRawRequest(**req_a.model_dump())

        self.assertEqual(req_a.chave_deterministica(), req_b.chave_deterministica())


if __name__ == "__main__":
    unittest.main()
