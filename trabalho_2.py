import math
import turtle
from desenho import desenhar, abrir_janela
from transformacao import transformar, inversa

# Mostra a pergunta e le um numero digitado pelo usuario.
# Se ele digitar algo que nao e numero (ex: "abc"), avisa e pergunta de novo,
# ate receber um valor valido. Retorna o numero como float.
def ler_numero(pergunta) -> float:
    while True:
        try:
            return float(input(pergunta).replace(',', '.'))  # aceita tanto ponto quanto virgula
        except ValueError:
            print("Entrada invalida! Digite um numero.")

# Mostra a matriz 2x2 com duas casas decimais, uma linha por vez.
# O round(...) + 0.0 evita aparecer "-0.00" (ex: -0.0 ou -0.0000000001).
def mostrar_matriz(titulo: str, m: list[list[float]]) -> None:
    print(titulo)
    for lin in m:
        a = round(lin[0], 2) + 0.0
        b = round(lin[1], 2) + 0.0
        print(f"  [{a:.2f} {b:.2f} ]")

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

# pergunta ao usuario quantas transformacoes ele quer aplicar, e le cada uma delas. 
# A cada transformacao, a figura atual e multiplicada pela matriz correspondente, e a matriz e guardada na lista de matrizes.

while True:
    try:
        num_transformacoes = int(input("Quantas transformacoes deseja aplicar? "))
        if num_transformacoes < 0:
            print("O numero de transformacoes deve ser zero ou positivo!")
            continue
        elif num_transformacoes == 0:
            print("Nenhuma transformação será aplicada.")
        else:
            print(f"Voce podera aplicar {num_transformacoes} transformacoes.")
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

abrir_janela()  # abre a janela do turtle para desenhar

# centro da figura = media dos x e media dos y
cx = 0
cy = 0
for x, y in pontos:
    cx = cx + x
    cy = cy + y
cx = cx / n
cy = cy / n

# Guarda so a figura original e a atual. Cada transformacao fica registrada
# em matrizes (e o nome em nomes); para reverter, aplica na figura atual a
# matriz inversa de cada uma, da ultima para tras.
original = pontos
atual = pontos
nomes = []
matrizes = []

# loop principal: a cada volta desenha as figuras, mostra o menu e aplica
# a opcao escolhida, ate o usuario digitar 0. Se nenhuma transformacao foi
# pedida, nem entra no loop e vai direto mostrar a figura original.
while num_transformacoes > 0:
    # so desenha a figura atual (azul) se ja tiver alguma transformacao
    desenhar([original, atual] if len(nomes) > 0 else [original])

    # mostra os pontos da figura atual e as transformacoes ja feitas
    print()
    print("Figura atual:")
    for x, y in atual:
        print(f"  ({x:.2f}, {y:.2f})")

    if len(nomes) == 0:
        print("Nenhuma transformacao aplicada.")
    else:
        print("Transformacoes aplicadas:")
        for i in range(len(nomes)):
            print(f"  {i + 1}. {nomes[i]}")

    print()
    if len(nomes) < num_transformacoes:
        print(f"Transformacao {len(nomes) + 1} de {num_transformacoes}:")
    else:
        print(f"Limite de {num_transformacoes} transformacoes atingido.")

    print("1 - Rotacao")
    print("2 - Escala")
    print("3 - Reflexao")
    print("4 - Reverter ate uma transformacao anterior")
    print("0 - Sair")
    op = input("Escolha: ")

    # as opcoes 1, 2 e 3 aplicam uma transformacao nova, entao so valem
    # enquanto nao chegou no numero de transformacoes pedido
    if op in ("1", "2", "3") and len(nomes) >= num_transformacoes:
        print("Todas as transformacoes pedidas ja foram aplicadas. Reverta alguma para aplicar outra.")
        continue

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
        # reverter: volta para a figura de depois da transformacao k aplicando a
        # inversa de cada transformacao feita depois dela, da ultima para tras
        # (ex: voltar para a 1 aplica a inversa da 3 e depois a inversa da 2)
        if len(nomes) == 0:
            print("Nao tem nada para reverter!")
            continue
        try:
            k = int(input(f"Voltar para qual transformacao? (0 a {len(nomes) - 1}, 0 = figura original): "))
        except ValueError:
            print("Entrada invalida! Digite um numero inteiro.")
            continue
        if not 0 <= k < len(nomes):
            print("Numero invalido! Escolha um numero entre 0 e", len(nomes) - 1)
            continue

        # verifica se alguma das transformacoes a reverter nao tem inversa (det = 0)
        sem_inversa = []
        for j in range(k, len(matrizes)):
            if inversa(matrizes[j]) is None:
                sem_inversa.append(j)

        if len(sem_inversa) > 0:
            for j in sem_inversa:
                print(f"A transformacao {j + 1} ({nomes[j]}) tem det = 0, entao nao tem inversa e nao pode ser revertida.")
            continue
        
        # aplica a inversa na figura atual; o resultado e a figura de antes
        # daquela transformacao
        while len(nomes) > k:
            inv = inversa(matrizes.pop())
            atual = transformar(atual, inv, cx, cy)
            print("Revertendo:", nomes.pop())
            mostrar_matriz("Matriz inversa usada:", inv)
        continue

    elif op == "0":
        break

    else:
        print("Opcao invalida!")
        continue

    # so chega aqui nas opcoes 1, 2 e 3 (as outras usam continue ou break):
    # aplica a matriz na figura atual, guarda a matriz e mostra ela
    atual = transformar(atual, matriz, cx, cy)
    nomes.append(nome)
    matrizes.append(matriz)
    mostrar_matriz("Matriz usada:", matriz)

# desenha o resultado da ultima transformacao e deixa a janela aberta
# ate o usuario fechar (sem isso o programa termina e a janela some)
desenhar([original, atual] if len(nomes) > 0 else [original])

print("Feche a janela do desenho para encerrar.")
turtle.done()
