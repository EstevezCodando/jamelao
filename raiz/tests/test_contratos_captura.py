import unittest

from raiz.chave import chave_deterministica
from raiz.provedores import PROVEDORES


class TestChaveDeterministica(unittest.TestCase):
    def test_mesma_entrada_gera_mesma_chave(self) -> None:
        a = chave_deterministica(provedor="remoteok", url_absoluta="https://remoteok.com/jobs")
        b = chave_deterministica(provedor="remoteok", url_absoluta="https://remoteok.com/jobs")
        self.assertEqual(a, b)

    def test_provedor_diferente_gera_chave_diferente(self) -> None:
        a = chave_deterministica(provedor="remoteok", url_absoluta="https://remoteok.com/jobs")
        b = chave_deterministica(provedor="outro",    url_absoluta="https://remoteok.com/jobs")
        self.assertNotEqual(a, b)

    def test_url_diferente_gera_chave_diferente(self) -> None:
        a = chave_deterministica(provedor="remoteok", url_absoluta="https://remoteok.com/jobs")
        b = chave_deterministica(provedor="remoteok", url_absoluta="https://remoteok.com/outro")
        self.assertNotEqual(a, b)

    def test_chave_tem_64_caracteres(self) -> None:
        chave = chave_deterministica(provedor="remoteok", url_absoluta="https://remoteok.com/jobs")
        self.assertEqual(len(chave), 64)

    def test_chave_e_hexadecimal(self) -> None:
        chave = chave_deterministica(provedor="remoteok", url_absoluta="https://remoteok.com/jobs")
        self.assertRegex(chave, r"^[0-9a-f]{64}$")


class TestProvedor(unittest.TestCase):
    def test_remoteok_existe_no_mapa(self) -> None:
        self.assertIn("remoteok", PROVEDORES)

    def test_url_absoluta_monta_corretamente(self) -> None:
        p = PROVEDORES["remoteok"]
        self.assertEqual(p.url_absoluta, f"https://{p.host}{p.caminho}")

    def test_caminho_inicia_com_barra(self) -> None:
        self.assertTrue(PROVEDORES["remoteok"].caminho.startswith("/"))

    def test_provedor_e_imutavel(self) -> None:
        with self.assertRaises(Exception):
            PROVEDORES["remoteok"].nome = "outro"  # type: ignore[misc]


if __name__ == "__main__":
    unittest.main()
