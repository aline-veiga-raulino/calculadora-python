import tkinter as tk


janela = tk.Tk()
janela.title("Calculadora da Aline")
janela.geometry("350x500")
janela.minsize(300, 450)
janela.resizable(True, True)
janela.configure(bg="#18161f")


expressao = ""
resultado = tk.StringVar(value="0")


def atualizar_visor():
    resultado.set(expressao if expressao else "0")


def adicionar(valor):
    global expressao

    expressao += valor
    atualizar_visor()


def limpar():
    global expressao

    expressao = ""
    atualizar_visor()


def apagar():
    global expressao

    expressao = expressao[:-1]
    atualizar_visor()


def calcular_expressao(conta):
    tokens = []
    numero = ""

    for caractere in conta:
        if caractere.isdigit() or caractere == ".":
            numero += caractere

        else:
            if numero:
                tokens.append(float(numero))
                numero = ""

            if caractere in "+-*/()":
                tokens.append(caractere)

    if numero:
        tokens.append(float(numero))

    valores = []
    operadores = []

    prioridade = {
        "+": 1,
        "-": 1,
        "*": 2,
        "/": 2
    }

    def aplicar_operacao():
        operador = operadores.pop()
        direita = valores.pop()
        esquerda = valores.pop()

        if operador == "+":
            valores.append(esquerda + direita)

        elif operador == "-":
            valores.append(esquerda - direita)

        elif operador == "*":
            valores.append(esquerda * direita)

        elif operador == "/":
            if direita == 0:
                raise ZeroDivisionError

            valores.append(esquerda / direita)

    anterior = None

    for token in tokens:
        if isinstance(token, float):
            valores.append(token)
            anterior = "numero"

        elif token == "(":
            operadores.append(token)
            anterior = "abre"

        elif token == ")":
            while operadores and operadores[-1] != "(":
                aplicar_operacao()

            if not operadores:
                raise ValueError

            operadores.pop()
            anterior = "fecha"

        elif token in "+-*/":
            if token in "+-" and (
                anterior is None
                or anterior == "operador"
                or anterior == "abre"
            ):
                valores.append(0.0)

            while (
                operadores
                and operadores[-1] != "("
                and prioridade[operadores[-1]] >= prioridade[token]
            ):
                aplicar_operacao()

            operadores.append(token)
            anterior = "operador"

        else:
            raise ValueError

    while operadores:
        if operadores[-1] == "(":
            raise ValueError

        aplicar_operacao()

    if len(valores) != 1:
        raise ValueError

    return valores[0]


def calcular():
    global expressao

    try:
        if not expressao:
            return

        conta = expressao.replace("×", "*").replace("÷", "/")
        resultado_calculo = calcular_expressao(conta)

        if resultado_calculo.is_integer():
            resultado_calculo = int(resultado_calculo)

        expressao = str(resultado_calculo)
        atualizar_visor()

    except ZeroDivisionError:
        expressao = ""
        resultado.set("Erro: divisão por zero")

    except (ValueError, OverflowError):
        expressao = ""
        resultado.set("Erro")


def pressionar_tecla(evento):
    tecla = evento.keysym
    caractere = evento.char

    if caractere in "0123456789":
        adicionar(caractere)

    elif caractere in "+-*/":
        if caractere == "*":
            adicionar("×")
        elif caractere == "/":
            adicionar("÷")
        else:
            adicionar(caractere)

    elif caractere in ".,":
        adicionar(".")

    elif caractere in "()":
        adicionar(caractere)

    elif tecla == "Return":
        calcular()

    elif tecla == "BackSpace":
        apagar()

    elif tecla == "Escape":
        limpar()


visor = tk.Label(
    janela,
    textvariable=resultado,
    font=("Arial", 32, "bold"),
    anchor="e",
    padx=15,
    pady=20,
    bg="#18161f",
    fg="white"
)

visor.pack(
    fill="both",
    expand=True
)


frame_botoes = tk.Frame(
    janela,
    bg="#18161f"
)

frame_botoes.pack(
    fill="both",
    expand=True
)


botoes = [
    ["C", "⌫", "(", ")"],
    ["7", "8", "9", "÷"],
    ["4", "5", "6", "×"],
    ["1", "2", "3", "-"],
    ["0", ".", "=", "+"]
]


for linha, botoes_linha in enumerate(botoes):

    for coluna, texto in enumerate(botoes_linha):

        if texto == "C":
            comando = limpar

        elif texto == "⌫":
            comando = apagar

        elif texto == "=":
            comando = calcular

        else:
            comando = lambda valor=texto: adicionar(valor)

        if texto in ["÷", "×", "-", "+"]:
            cor = "#8b5cf6"

        elif texto == "=":
            cor = "#a78bfa"

        elif texto == "C":
            cor = "#ef4444"

        else:
            cor = "#292631"

        botao = tk.Button(
            frame_botoes,
            text=texto,
            command=comando,
            font=("Arial", 18, "bold"),
            bg=cor,
            fg="white",
            activebackground=cor,
            activeforeground="white",
            relief="flat",
            borderwidth=0,
            cursor="hand2"
        )

        botao.grid(
            row=linha,
            column=coluna,
            sticky="nsew",
            padx=4,
            pady=4
        )

        botao.bind(
            "<Enter>",
            lambda evento, cor=cor:
            evento.widget.configure(bg="#6d4bc1")
        )

        botao.bind(
            "<Leave>",
            lambda evento, cor=cor:
            evento.widget.configure(bg=cor)
        )


for coluna in range(4):
    frame_botoes.columnconfigure(
        coluna,
        weight=1
    )

for linha in range(5):
    frame_botoes.rowconfigure(
        linha,
        weight=1
    )


janela.bind(
    "<Key>",
    pressionar_tecla
)


janela.mainloop()