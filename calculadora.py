

import flet as ft
import re
from decimal import Decimal

botoes = [
    {'operador': 'AC', 'fonte': ft.Colors.WHITE, 'fundo': ft.Colors.PURPLE_900},
    {'operador': '±', 'fonte': ft.Colors.BLACK, 'fundo': ft.Colors.YELLOW_900},
    {'operador': '%', 'fonte': ft.Colors.BLACK, 'fundo': ft.Colors.YELLOW_800},
    {'operador': '÷', 'fonte': ft.Colors.BLACK, 'fundo': ft.Colors.YELLOW_700},
    {'operador': '7', 'fonte': ft.Colors.BLACK, 'fundo': ft.Colors.BLUE_GREY_100},
    {'operador': '8', 'fonte': ft.Colors.BLACK, 'fundo': ft.Colors.BLUE_GREY_100},
    {'operador': '9', 'fonte': ft.Colors.BLACK, 'fundo': ft.Colors.BLUE_GREY_100},
    {'operador': '×', 'fonte': ft.Colors.BLACK, 'fundo': ft.Colors.YELLOW_700},
    {'operador': '4', 'fonte': ft.Colors.BLACK, 'fundo': ft.Colors.BLUE_GREY_100},
    {'operador': '5', 'fonte': ft.Colors.BLACK, 'fundo': ft.Colors.BLUE_GREY_100},
    {'operador': '6', 'fonte': ft.Colors.BLACK, 'fundo': ft.Colors.BLUE_GREY_100},
    {'operador': '-', 'fonte': ft.Colors.BLACK, 'fundo': ft.Colors.YELLOW_800},
    {'operador': '1', 'fonte': ft.Colors.BLACK, 'fundo': ft.Colors.BLUE_GREY_100},
    {'operador': '2', 'fonte': ft.Colors.BLACK, 'fundo': ft.Colors.BLUE_GREY_100},
    {'operador': '3', 'fonte': ft.Colors.BLACK, 'fundo': ft.Colors.BLUE_GREY_100},
    {'operador': '+', 'fonte': ft.Colors.BLACK, 'fundo': ft.Colors.YELLOW_900},
    {'operador': '0', 'fonte': ft.Colors.BLACK, 'fundo': ft.Colors.BLUE_GREY_100},
    {'operador': ',', 'fonte': ft.Colors.BLACK, 'fundo': ft.Colors.BLUE_GREY_100},
    {'operador': '⌫', 'fonte': ft.Colors.WHITE, 'fundo': ft.Colors.PINK_700},
    {'operador': '=', 'fonte': ft.Colors.WHITE, 'fundo': ft.Colors.LIGHT_GREEN_700},
]


def formatar_numero(numero):
    try:
        valor = Decimal(str(numero))

        if valor == valor.to_integral_value():
            return f"{int(valor):,}".replace(",", ".")

        partes = format(valor, "f").split(".")

        inteiro = f"{int(partes[0]):,}".replace(",", ".")
        decimal = partes[1].rstrip("0")

        return inteiro + "," + decimal

    except (ValueError, TypeError):
        return str(numero)


def formatar_expressao(texto):
    partes = re.split(r'([+\-×÷*/%])', texto)

    for i, parte in enumerate(partes):
        if not parte:
            continue

        if "," in parte:
            inteiro, decimal = parte.split(",", 1)

            if inteiro.isdigit():
                inteiro = f"{int(inteiro):,}".replace(",", ".")

            partes[i] = inteiro + "," + decimal

        elif parte.isdigit():
            partes[i] = f"{int(parte):,}".replace(",", ".")

    return "".join(partes)


def calculate(expression):
    try:
        expression = expression.replace(".", "")
        expression = expression.replace(",", ".")
        expression = expression.replace("×", "*")
        expression = expression.replace("÷", "/")
        expression = re.sub(
            r'(\d+(?:\.\d+)?)%(\d+(?:\.\d+)?)',
            r'(\1/100*\2)',
            expression
        )

        expression = re.sub(
            r'(\d+(?:\.\d+)?)%',
            r'(\1/100)',
            expression
        )

        value = eval(expression)

        return formatar_numero(value)

    except ZeroDivisionError:
        return "Erro: divisão por zero"

    except Exception as erro:
        print("Erro no cálculo:", erro)
        return "Error"


def main(page: ft.Page):

    page.bgcolor = "#000000FF"
    page.window.resizable = False
    page.window.width = 350
    page.window.height = 500
    page.window.min_width = 300
    page.window.min_height = 400
    page.title = "Calculadora"
    page.window.always_on_top = True

    def filtrar_teclado(e):
        texto = e.control.value or ""

        # Aceita números, vírgula e operadores
        permitido = re.sub(r'[^0-9,+\-×÷*/%]', '', texto)

        e.control.value = formatar_expressao(permitido)
        e.control.update()

    result = ft.TextField(
        value='0',
        color=ft.Colors.WHITE,
        text_size=30,
        read_only=False,
        text_align=ft.TextAlign.RIGHT,
        border=ft.InputBorder.NONE,
        width=300,
        on_change=filtrar_teclado
    )

    def select(e):

        value = e.control.content.value
        current = result.value

        if value == "AC":
            result.value = "0"

        elif value == "=":
            result.value = calculate(current)

        elif value == "±":
            try:
                if not re.search(r'[+\-×÷*/%]', current):
                    numero = Decimal(
                        current.replace(".", "").replace(",", ".")
                    )

                    if numero != 0:
                        numero = -numero
                        result.value = formatar_numero(numero)

            except Exception:
                pass

        elif value == "%":
            if current and current[-1].isdigit():
                result.value += "%"

        elif value.isdigit():

            if current == "0" or current.startswith("Erro") or current == "Error":
                result.value = value

            else:
                # Remove os pontos antes de acrescentar o próximo algarismo
                atual = current.replace(".", "")
                result.value = atual + value

            # Aplica novamente a formatação de milhares
            result.value = formatar_expressao(result.value)

        elif value == ",":

            parte_atual = re.split(
                r'[+\-×÷*/%]', current
            )[-1]

            if "," not in parte_atual:
                result.value = current + ","

        elif value == "⌫":

            atual = current.replace(".", "")

            if len(atual) > 1:
                result.value = formatar_expressao(atual[:-1])
            else:
                result.value = "0"

        else:

            if current == "0":
                if value == "-":
                    result.value = "-"
                else:
                    return

            elif current and current[-1] in ["+", "-", "×", "÷", "*", "/"]:
                result.value = current[:-1] + value

            else:
                result.value += value

        result.update()

    display = ft.Row(
        width=300,
        controls=[result],
        alignment=ft.MainAxisAlignment.END
    )

    btn = [
        ft.Container(
            content=ft.Text(
                value=botao['operador'],
                color=botao['fonte']
            ),
            width=65,
            height=65,
            bgcolor=botao['fundo'],
            border_radius=100,
            alignment=ft.Alignment.CENTER,
            on_click=select
        )
        for botao in botoes
    ]

    keyboard = ft.Row(
        width=300,
        wrap=True,
        spacing=8,
        run_spacing=8,
        controls=btn,
        alignment=ft.MainAxisAlignment.END
    )

    page.add(display, keyboard)


ft.run(main)
