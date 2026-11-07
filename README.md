# Calculadora em Python

Calculadora de linha de comando, segura (não usa `eval`), com suporte a vírgula decimal.

## Uso

```bash
# Expressão direta
python3 calculadora.py "1500 * 1,01 ** 12"     # juros compostos: 1690.237545198

# Modo interativo
python3 calculadora.py
>>> 10 * 3
= 30
>>> ans / 4
= 7.5
```

**Operadores:** `+ - * / // % **` · **Funções:** `raiz(x)`, `abs(x)`, `arred(x; casas)`, `log(x)`, `log10(x)` · **Constantes:** `pi`, `e` · **`ans`** = último resultado.

## Testes

```bash
python3 -m unittest -v
```

## Linter

```bash
pip install -r requirements-dev.txt
ruff check .
```
