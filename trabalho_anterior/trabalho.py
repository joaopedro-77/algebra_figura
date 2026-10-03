import math
from desenho import desenhar, transformar 

# Mostra a pergunta e le um numero digitado pelo usuario.
# Se ele digitar algo que nao e numero (ex: "abc"), avisa e pergunta de novo,
# ate receber um valor valido. Retorna o numero como float.
def ler_numero(pergunta) -> float:
    while True:
        try:
            return float(input(pergunta).replace(',', '.'))  # aceita tanto ponto quanto virgula
        except ValueError:
            print("Entrada invalida! Digite um numero.")

print("===== TRANSFORMACOES GEOMETRICAS 2D =====")

# le quantos pontos a figura tem (tem que ser um inteiro maior que zero)
while True:
    try:
        n = int(input("Quantos pontos tem a figura? "))
        if n <= 0:
            print("O numero de pontos deve ser positivo!")
            continue
        break
    except ValueError:
        print("Entrada invalida! Digite um numero inteiro.")

# le as coordenadas de cada ponto e guarda na lista como (x, y)
pontos = []
for i in range(n):
    print(f"Ponto {i + 1}:")
    x = ler_numero(" x = ")
    y = ler_numero(" y = ")
    pontos.append((x, y))

# centro da figura = media dos x e media dos y
cx = 0
cy = 0
for x, y in pontos:
    cx = cx + x
    cy = cy + y
cx = cx / n
cy = cy / n

# figuras[0] e a original e figuras[-1] e a atual.
# Cada transformacao coloca uma figura nova no fim da lista, entao para
# desfazer e so tirar a ultima (nao precisa de matriz inversa).
figuras = [pontos]
nomes = []

# loop principal: a cada volta desenha as figuras, mostra o menu e aplica
# a opcao escolhida, ate o usuario digitar 0
while True:
    desenhar(figuras)

    # mostra os pontos da figura atual e as transformacoes ja feitas
    print()
    print("Figura atual:")
    for x, y in figuras[-1]:
        print(f"  ({x:.2f}, {y:.2f})")

    if len(nomes) == 0:
        print("Nenhuma transformacao aplicada.")
    else:
        print("Transformacoes aplicadas:")
        for i in range(len(nomes)):
            print(f"  {i + 1}. {nomes[i]}")

    print()
    print("1 - Rotacao")
    print("2 - Escala")
    print("3 - Reflexao")
    print("4 - Desfazer a ultima")
    print("0 - Sair")
    op = input("Escolha: ")

    if op == "1":
        # rotacao: gira a figura pelo angulo digitado (positivo = sentido
        # anti-horario). math.cos e math.sin usam radianos, por isso a conversao.
        graus = ler_numero("Angulo (graus): ")
        a = math.radians(graus)
        matriz = [[math.cos(a), -math.sin(a)],
                  [math.sin(a), math.cos(a)]]
        nome = f"Rotacao de {graus} graus"

    elif op == "2":
        # escala: multiplica a distancia ao centro por sx na horizontal e por
        # sy na vertical (maior que 1 aumenta, entre 0 e 1 diminui)
        sx = ler_numero("Escala em x: ")
        sy = ler_numero("Escala em y: ")
        matriz = [[sx, 0],
                  [0, sy]]
        nome = f"Escala ({sx}, {sy})"

    elif op == "3":
        # reflexao: escolhe a matriz de espelhamento de acordo com o eixo digitado
        eixo = input("Refletir em qual? (x, y, o = origem, d = reta y=x): ")
        if eixo == "x":
            matriz = [[1, 0], [0, -1]]
            nome = "Reflexao no eixo X"
        elif eixo == "y":
            matriz = [[-1, 0], [0, 1]]
            nome = "Reflexao no eixo Y"
        elif eixo == "o":
            matriz = [[-1, 0], [0, -1]]
            nome = "Reflexao na origem"
        elif eixo == "d":
            matriz = [[0, 1], [1, 0]]
            nome = "Reflexao na reta y=x"
        else:
            print("Opcao invalida!")
            continue

    elif op == "4":
        # desfazer: tira a ultima figura e o nome da ultima transformacao
        if len(nomes) == 0:
            print("Nao tem nada para desfazer!")
        else:
            figuras.pop()
            print("Desfeito:", nomes.pop())
        continue

    elif op == "0":
        break

    else:
        print("Opcao invalida!")
        continue

    # so chega aqui nas opcoes 1, 2 e 3 (as outras usam continue ou break):
    # aplica a matriz na figura atual, guarda o resultado e mostra a matriz
    nova = transformar(figuras[-1], matriz, cx, cy)
    figuras.append(nova)
    nomes.append(nome)
    print("Matriz usada:")
    for lin in matriz:
        print(f"  [{lin[0]:.2f} {lin[1]:.2f} ]")

print("Fim!")