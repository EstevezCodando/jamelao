import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, call, patch

from raiz.core import (
    _processar_pagina,
    baixar_para_arquivo,
    coletar,
    contar_linhas,
    escrever_jsonl_se_nao_existir,
)
from raiz.provedores import Provedor
from raiz.remoteok import extrair as extrair_remoteok

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

HTML_VAZIO = "<html><body></body></html>"


def _provedor_teste(extrair=extrair_remoteok):
    return Provedor(
        nome="teste",
        host="exemplo.com",
        proxima_pagina=lambda p: f"/vagas?offset={p * 10}",
        extrair=extrair,
    )


# ---------------------------------------------------------------------------
# baixar_para_arquivo
# ---------------------------------------------------------------------------

class TestBaixarParaArquivo(unittest.TestCase):
    def test_nao_baixa_se_arquivo_ja_existe(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            destino = Path(tmp) / "captura.html"
            destino.write_bytes(b"conteudo anterior")

            with patch("http.client.HTTPSConnection") as mock_conn:
                baixar_para_arquivo(host="exemplo.com", caminho="/vagas", expected_status=200, destino=destino)
                mock_conn.assert_not_called()

            self.assertEqual(destino.read_bytes(), b"conteudo anterior")

    def test_baixa_e_grava_quando_arquivo_nao_existe(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            destino = Path(tmp) / "captura.html"

            mock_resposta = MagicMock()
            mock_resposta.status = 200
            mock_resposta.read.return_value = b""

            mock_conn = MagicMock()
            mock_conn.getresponse.return_value = mock_resposta

            with patch("http.client.HTTPSConnection", return_value=mock_conn):
                with patch("shutil.copyfileobj") as mock_copy:
                    baixar_para_arquivo(host="exemplo.com", caminho="/vagas", expected_status=200, destino=destino)
                    mock_conn.request.assert_called_once_with("GET", "/vagas")
                    mock_copy.assert_called_once()

    def test_lanca_erro_em_status_inesperado(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            destino = Path(tmp) / "captura.html"

            mock_resposta = MagicMock()
            mock_resposta.status = 404

            mock_conn = MagicMock()
            mock_conn.getresponse.return_value = mock_resposta

            with patch("http.client.HTTPSConnection", return_value=mock_conn):
                with self.assertRaises(RuntimeError) as ctx:
                    baixar_para_arquivo(host="exemplo.com", caminho="/vagas", expected_status=200, destino=destino)

            self.assertIn("404", str(ctx.exception))


# ---------------------------------------------------------------------------
# escrever_jsonl_se_nao_existir
# ---------------------------------------------------------------------------

class TestEscreverJsonlSeNaoExistir(unittest.TestCase):
    def test_grava_registros_em_jsonl(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            destino = Path(tmp) / "saida.jsonl"
            registros = [{"title": "Dev"}, {"title": "QA"}]

            escrever_jsonl_se_nao_existir(destino=destino, registros=registros)

            linhas = destino.read_text(encoding="utf-8").strip().splitlines()
            self.assertEqual(len(linhas), 2)
            self.assertEqual(json.loads(linhas[0])["title"], "Dev")
            self.assertEqual(json.loads(linhas[1])["title"], "QA")

    def test_nao_sobrescreve_arquivo_existente(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            destino = Path(tmp) / "saida.jsonl"
            destino.write_text('{"title": "original"}\n', encoding="utf-8")

            escrever_jsonl_se_nao_existir(destino=destino, registros=[{"title": "novo"}])

            conteudo = destino.read_text(encoding="utf-8")
            self.assertIn("original", conteudo)
            self.assertNotIn("novo", conteudo)

    def test_grava_lista_vazia(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            destino = Path(tmp) / "saida.jsonl"

            escrever_jsonl_se_nao_existir(destino=destino, registros=[])

            self.assertTrue(destino.exists())
            self.assertEqual(destino.read_text(encoding="utf-8"), "")


# ---------------------------------------------------------------------------
# contar_linhas
# ---------------------------------------------------------------------------

class TestContarLinhas(unittest.TestCase):
    def test_conta_linhas_nao_vazias(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            arquivo = Path(tmp) / "dados.jsonl"
            arquivo.write_text('{"a": 1}\n{"b": 2}\n{"c": 3}\n', encoding="utf-8")

            self.assertEqual(contar_linhas(arquivo), 3)

    def test_ignora_linhas_vazias(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            arquivo = Path(tmp) / "dados.jsonl"
            arquivo.write_text('{"a": 1}\n\n{"b": 2}\n\n', encoding="utf-8")

            self.assertEqual(contar_linhas(arquivo), 2)

    def test_arquivo_vazio_retorna_zero(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            arquivo = Path(tmp) / "dados.jsonl"
            arquivo.write_text("", encoding="utf-8")

            self.assertEqual(contar_linhas(arquivo), 0)


# ---------------------------------------------------------------------------
# _processar_pagina
# ---------------------------------------------------------------------------

class TestProcessarPagina(unittest.TestCase):
    def test_retorna_quantidade_de_registros_gravados(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pasta = Path(tmp)
            provedor = _provedor_teste()

            pasta_html = pasta / "captura.html"
            pasta_html.write_text(HTML_COM_JOB, encoding="utf-8")

            with patch("raiz.core.baixar_para_arquivo"):
                resultado = _processar_pagina(provedor, pasta, "/vagas?offset=0")

            self.assertEqual(resultado, 1)

    def test_retorna_zero_para_html_sem_jobs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pasta = Path(tmp)
            provedor = _provedor_teste()

            (pasta / "captura.html").write_text(HTML_VAZIO, encoding="utf-8")

            with patch("raiz.core.baixar_para_arquivo"):
                resultado = _processar_pagina(provedor, pasta, "/vagas?offset=0")

            self.assertEqual(resultado, 0)

    def test_nao_regrava_jsonl_existente(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pasta = Path(tmp)
            provedor = _provedor_teste()

            (pasta / "captura.html").write_text(HTML_COM_JOB, encoding="utf-8")
            (pasta / "extracao.jsonl").write_text('{"title": "original"}\n', encoding="utf-8")

            with patch("raiz.core.baixar_para_arquivo"):
                _processar_pagina(provedor, pasta, "/vagas?offset=0")

            conteudo = (pasta / "extracao.jsonl").read_text(encoding="utf-8")
            self.assertIn("original", conteudo)


# ---------------------------------------------------------------------------
# coletar
# ---------------------------------------------------------------------------

class TestColetar(unittest.TestCase):
    def test_para_quando_pagina_retorna_zero_registros(self) -> None:
        provedor = _provedor_teste()

        with patch("raiz.core._processar_pagina", return_value=0) as mock_proc:
            with tempfile.TemporaryDirectory() as tmp:
                coletar(provedor, pasta_raiz=Path(tmp), limite_paginas=5)

            # deve ter chamado só uma vez — parou na primeira página vazia
            self.assertEqual(mock_proc.call_count, 1)

    def test_pagina_todas_ate_o_limite(self) -> None:
        provedor = _provedor_teste()

        with patch("raiz.core._processar_pagina", return_value=10) as mock_proc:
            with tempfile.TemporaryDirectory() as tmp:
                coletar(provedor, pasta_raiz=Path(tmp), limite_paginas=3)

            self.assertEqual(mock_proc.call_count, 3)

    def test_cria_pasta_para_cada_pagina(self) -> None:
        provedor = _provedor_teste()

        with patch("raiz.core._processar_pagina", return_value=1):
            with tempfile.TemporaryDirectory() as tmp:
                pasta_raiz = Path(tmp)
                coletar(provedor, pasta_raiz=pasta_raiz, limite_paginas=2)

                pastas = list((pasta_raiz / "teste").iterdir())
                self.assertEqual(len(pastas), 2)

    def test_paginas_diferentes_geram_pastas_diferentes(self) -> None:
        provedor = _provedor_teste()

        with patch("raiz.core._processar_pagina", return_value=1):
            with tempfile.TemporaryDirectory() as tmp:
                pasta_raiz = Path(tmp)
                coletar(provedor, pasta_raiz=pasta_raiz, limite_paginas=2)

                pastas = [p.name for p in (pasta_raiz / "teste").iterdir()]
                self.assertEqual(len(pastas), len(set(pastas)))


if __name__ == "__main__":
    unittest.main()