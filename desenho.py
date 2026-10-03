# Trabalho de Algebra Linear - Transformacoes geometricas 2D
#
# O usuario digita os pontos de uma figura e aplica rotacao, escala e
# reflexao nela. Cada transformacao e uma matriz 2x2 que multiplica os pontos.
#
# Para rodar: python3 trabalho.py
import turtle

# Desenha um segmento de reta de (x1, y1) ate (x2, y2). A caneta e levantada
# antes de ir ao primeiro ponto para nao riscar o caminho ate la.
def linha(x1: float, y1: float, x2: float, y2: float) -> None:
    turtle.penup()
    turtle.goto(x1, y1)
    turtle.pendown()
    turtle.goto(x2, y2)


# Desenha uma figura na cor dada: liga os pontos na ordem em que foram
# digitados, fecha o contorno e escreve a coordenada de cada vertice.
def desenhar_figura(pontos: list[tuple[float, float]], cor: str) -> None:
    turtle.color(cor)
    # contorno
    turtle.penup()
    turtle.goto(pontos[0])
    turtle.pendown()
    for p in pontos:
        turtle.goto(p)
    turtle.goto(pontos[0])  # volta pro primeiro ponto pra fechar a figura
    # uma bolinha e a coordenada em cada vertice
    for x, y in pontos:
        turtle.penup()
        turtle.goto(x, y)
        turtle.dot(8)
        turtle.write(f"  ({x:.2f}, {y:.2f})", font=("Arial", 10, "normal"))


# Redesenha a tela toda: apaga o desenho anterior, ajusta a escala para as
# figuras caberem, desenha os eixos numerados, a figura original em cinza e,
# se ja houve alguma transformacao, a figura atual em azul.
def desenhar(figuras: list[list[tuple[float, float]]]) -> None:
    original = figuras[0]
    atual = figuras[-1]

    # o tamanho da tela e o ponto mais longe da origem, mais uma folga
    t = 0
    for x, y in original + atual:
        t = max(t, abs(x), abs(y))
    t = t * 1.3
 
    turtle.clear()
    turtle.setworldcoordinates(-t, -t, t, t)
    turtle.hideturtle()
    turtle.width(2)

    # eixos x e y
    turtle.color("lightgray")
    linha(-t, 0, t, 0)
    linha(0, -t, 0, t)

    # numeros nos eixos. O passo cresce junto com a tela para os numeros
    # nao ficarem amontoados (tela pequena: 1, 2, 3... tela grande: 2, 4, 6...)
    passo = int(t / 5) + 1
    turtle.color("gray")
    for i in range(-int(t), int(t) + 1):
        if i % passo == 0 and i != 0:
            turtle.penup()
            turtle.goto(i, 0)  # no eixo x
            turtle.dot(4)
            turtle.write(i, font=("Arial", 8, "normal"))
            turtle.goto(0, i)  # no eixo y
            turtle.dot(4)
            turtle.write(i, font=("Arial", 8, "normal"))

    desenhar_figura(original, "gray")
    if len(figuras) > 1:
        desenhar_figura(atual, "blue")
    turtle.update()

# configura a janela do turtle; roda uma vez so, quando o trabalho.py
# importa este arquivo
def abrir_janela() -> None:
    turtle.setup(650, 650)
    turtle.title("Cinza = figura original    Azul = figura transformada")
    turtle.tracer(0) # desliga a animacao do turtle para desenhar mais rapido