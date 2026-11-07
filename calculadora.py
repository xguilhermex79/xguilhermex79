"""Calculadora em Python.

Dois modos de uso:
  1. Expressão livre:   python calculadora.py "2 + 3 * (4 - 1)"
  2. Modo interativo:   python calculadora.py

A avaliação de expressões usa o módulo `ast` (árvore sintática) em vez de
`eval()`, para aceitar SOMENTE números e operadores matemáticos — nunca
código arbitrário.
"""

import ast
import math
import operator
import sys

# Operadores permitidos: mapeia o nó da AST para a função correspondente.
OPERADORES_BINARIOS = {
    ast.Add: operator.add,        # +
    ast.Sub: operator.sub,        # -
    ast.Mult: operator.mul,       # *
    ast.Div: operator.truediv,    # /
    ast.FloorDiv: operator.floordiv,  # //
    ast.Mod: operator.mod,        # %
    ast.Pow: operator.pow,        # **
}

OPERADORES_UNARIOS = {
    ast.UAdd: operator.pos,       # +x
    ast.USub: operator.neg,       # -x
}

FUNCOES = {
    "sqrt": math.sqrt,
    "raiz": math.sqrt,
    "abs": abs,
    "round": round,
    "arred": round,
    "log": math.log,
    "log10": math.log10,
}

CONSTANTES = {
    "pi": math.pi,
    "e": math.e,
}

LIMITE_EXPOENTE = 1000  # evita contas gigantes como 9**9**9


def _avaliar_no(no):
    """Percorre a árvore da expressão recursivamente e calcula o resultado."""
    if isinstance(no, ast.Expression):
        return _avaliar_no(no.body)

    if isinstance(no, ast.Constant) and isinstance(no.value, (int, float)) \
            and not isinstance(no.value, bool):
        return no.value

    if isinstance(no, ast.BinOp) and type(no.op) in OPERADORES_BINARIOS:
        esquerda = _avaliar_no(no.left)
        direita = _avaliar_no(no.right)
        if isinstance(no.op, ast.Pow) and abs(direita) > LIMITE_EXPOENTE:
            raise ValueError("Expoente grande demais.")
        if isinstance(no.op, (ast.Div, ast.FloorDiv, ast.Mod)) and direita == 0:
            raise ZeroDivisionError("Divisão por zero não é permitida.")
        return OPERADORES_BINARIOS[type(no.op)](esquerda, direita)

    if isinstance(no, ast.UnaryOp) and type(no.op) in OPERADORES_UNARIOS:
        return OPERADORES_UNARIOS[type(no.op)](_avaliar_no(no.operand))

    if isinstance(no, ast.Name) and no.id in CONSTANTES:
        return CONSTANTES[no.id]

    if (isinstance(no, ast.Call) and isinstance(no.func, ast.Name)
            and no.func.id in FUNCOES and not no.keywords):
        argumentos = [_avaliar_no(arg) for arg in no.args]
        return FUNCOES[no.func.id](*argumentos)

    raise ValueError("Expressão inválida ou não permitida.")


def calcular(expressao: str):
    """Calcula uma expressão matemática em texto, ex.: '10 * (2 + 3)'.

    Aceita vírgula como separador decimal (padrão brasileiro): '2,5 * 2'.
    """
    expressao = expressao.strip()
    if not expressao:
        raise ValueError("Digite uma expressão.")
    # Troca vírgula decimal por ponto, ex.: "2,5" -> "2.5".
    # (Funções com vários argumentos devem usar ';', ex.: arred(3,14159; 2).)
    expressao = expressao.replace(",", ".").replace(";", ",")
    try:
        arvore = ast.parse(expressao, mode="eval")
    except SyntaxError:
        raise ValueError("Erro de sintaxe na expressão.") from None
    return _avaliar_no(arvore)


def formatar(numero) -> str:
    """Formata o resultado: inteiros sem casas decimais, reais com até 10."""
    if isinstance(numero, float) and numero.is_integer():
        numero = int(numero)
    if isinstance(numero, float):
        return f"{numero:.10f}".rstrip("0").rstrip(".")
    return str(numero)


AJUDA = """
Calculadora Python — digite uma expressão e pressione Enter.

  Operadores:  +  -  *  /  //  (divisão inteira)  %  (resto)  **  (potência)
  Funções:     raiz(x)  abs(x)  arred(x; casas)  log(x)  log10(x)
  Constantes:  pi  e
  Variável:    ans  (último resultado)
  Decimais:    use vírgula ou ponto — 2,5 ou 2.5

  Comandos:    ajuda  |  sair
"""


def modo_interativo():
    print(AJUDA)
    ultimo = 0
    while True:
        try:
            entrada = input(">>> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nAté logo!")
            break

        if entrada.lower() in ("sair", "exit", "quit", "q"):
            print("Até logo!")
            break
        if entrada.lower() in ("ajuda", "help", "?"):
            print(AJUDA)
            continue
        if not entrada:
            continue

        CONSTANTES["ans"] = ultimo
        try:
            ultimo = calcular(entrada)
            print(f"= {formatar(ultimo)}")
        except (ValueError, ZeroDivisionError, OverflowError, TypeError) as erro:
            print(f"Erro: {erro}")


def main():
    if len(sys.argv) > 1:
        try:
            print(formatar(calcular(" ".join(sys.argv[1:]))))
        except (ValueError, ZeroDivisionError, OverflowError, TypeError) as erro:
            print(f"Erro: {erro}", file=sys.stderr)
            sys.exit(1)
    else:
        modo_interativo()


if __name__ == "__main__":
    main()
