import unittest

from calculadora import calcular, formatar


class TestCalculadora(unittest.TestCase):
    def test_operacoes_basicas(self):
        self.assertEqual(calcular("2 + 3"), 5)
        self.assertEqual(calcular("10 - 4"), 6)
        self.assertEqual(calcular("6 * 7"), 42)
        self.assertEqual(calcular("9 / 2"), 4.5)
        self.assertEqual(calcular("9 // 2"), 4)
        self.assertEqual(calcular("9 % 2"), 1)
        self.assertEqual(calcular("2 ** 10"), 1024)

    def test_precedencia_e_parenteses(self):
        self.assertEqual(calcular("2 + 3 * 4"), 14)
        self.assertEqual(calcular("(2 + 3) * 4"), 20)
        self.assertEqual(calcular("-3 + 5"), 2)

    def test_virgula_decimal(self):
        self.assertEqual(calcular("2,5 * 2"), 5.0)

    def test_funcoes_e_constantes(self):
        self.assertEqual(calcular("raiz(16)"), 4.0)
        self.assertEqual(calcular("arred(3,14159; 2)"), 3.14)
        self.assertAlmostEqual(calcular("pi"), 3.141592653589793)

    def test_erros(self):
        with self.assertRaises(ZeroDivisionError):
            calcular("1 / 0")
        with self.assertRaises(ValueError):
            calcular("2 +")
        with self.assertRaises(ValueError):
            calcular("__import__('os')")
        with self.assertRaises(ValueError):
            calcular("9 ** 9 ** 9")

    def test_formatar(self):
        self.assertEqual(formatar(5.0), "5")
        self.assertEqual(formatar(0.1 + 0.2), "0.3")
        self.assertEqual(formatar(42), "42")


if __name__ == "__main__":
    unittest.main()
