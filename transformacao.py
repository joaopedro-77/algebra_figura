# Multiplica a matriz 2x2 por cada ponto (x, y) da figura.
# Antes de multiplicar, o centro da figura e levado para a origem, e depois
# volta para o lugar. Assim a figura gira e aumenta no proprio lugar.
def transformar(pontos: list[tuple[float, float]], m: list[list[float]], cx: float, cy: float) -> list[tuple[float, float]]:
    novos = []

    # p' = M·(p − c) + c.

    for x, y in pontos:
        x = x - cx
        y = y - cy
        novo_x = m[0][0] * x + m[0][1] * y
        novo_y = m[1][0] * x + m[1][1] * y
        novos.append((novo_x + cx, novo_y + cy))
    return novos

# Calcula a inversa da matriz 2x2 [[a, b], [c, d]]:
#   inversa = 1/det * [[d, -b], [-c, a]], com det = a*d - b*c
# Se det = 0 a matriz nao tem inversa (ex: escala com 0) e retorna None.
def inversa(m: list[list[float]]) -> list[list[float]] | None:
    a, b = m[0]
    c, d = m[1]
    det = a * d - b * c
    if det == 0:
        return None
    return [[d / det, -b / det],
            [-c / det, a / det]]

# det = 1 a area da figura nao muda; 
# det > 1 aumenta a area; 0 < det < 1 diminui a area;
# det < 0 inverte a figura (espelha) e aumenta/diminui a area de acordo com o valor absoluto do det.