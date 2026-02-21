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

    def test_url_absoluta_inicia_com_https(self) -> None:
        self.assertTrue(PROVEDORES["remoteok"].url_absoluta.startswith("https://"))

    def test_url_absoluta_contem_o_host(self) -> None:
        p = PROVEDORES["remoteok"]
        self.assertIn(p.host, p.url_absoluta)

    def test_proxima_pagina_retorna_caminho_relativo(self) -> None:
        p = PROVEDORES["remoteok"]
        self.assertTrue(p.proxima_pagina(0).startswith("/"))

    def test_proxima_pagina_difere_entre_paginas(self) -> None:
        p = PROVEDORES["remoteok"]
        self.assertNotEqual(p.proxima_pagina(0), p.proxima_pagina(1))

    def test_provedor_e_imutavel(self) -> None:
        with self.assertRaises(Exception):
            PROVEDORES["remoteok"].nome = "outro"  # type: ignore[misc]

    def test_provedor_tem_funcao_extrair(self) -> None:
        self.assertTrue(callable(PROVEDORES["remoteok"].extrair))

    def test_provedor_tem_funcao_proxima_pagina(self) -> None:
        self.assertTrue(callable(PROVEDORES["remoteok"].proxima_pagina))


if __name__ == "__main__":
    unittest.main()