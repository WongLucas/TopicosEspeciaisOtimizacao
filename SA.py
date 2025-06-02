import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# Definição do tamanho do container
CONTAINER_WIDTH = 10
CONTAINER_HEIGHT = 10

# Lista dos retângulos (largura, altura)
rectangles = [
    (4, 3), (3, 3), (5, 2), (2, 5), (3, 2),
    (2, 2), (4, 1), (1, 4), (2, 3), (3, 2)
]

# Função de empacotamento usando Shelf First Fit
def shelf_first_fit_placement(rect_list):
    positions = []
    shelf_y = 0
    shelf_height = 0
    shelf_used_width = 0

    for idx, (w, h) in enumerate(rect_list):
        if shelf_used_width + w > CONTAINER_WIDTH:
            shelf_y += shelf_height
            shelf_used_width = 0
            shelf_height = 0

        if shelf_y + h > CONTAINER_HEIGHT:
            break

        positions.append((idx, shelf_used_width, shelf_y, w, h))

        shelf_used_width += w
        if h > shelf_height:
            shelf_height = h

    return positions

# Função para desenhar o container e os retângulos
def draw_solution(positions, title="Container"):
    plt.figure(figsize=(6, 6))
    ax = plt.gca()
    for rect in positions:
        idx, x, y, w, h = rect
        ax.add_patch(Rectangle((x, y), w, h, edgecolor='black', facecolor='lightblue'))
        plt.text(x + w/2, y + h/2, str(idx), ha='center', va='center', fontsize=10)
    plt.xlim(0, CONTAINER_WIDTH)
    plt.ylim(0, CONTAINER_HEIGHT)
    plt.title(title)
    plt.gca().set_aspect('equal')
    #plt.gca().invert_yaxis()  # Remove se quiser mudar orientação
    plt.show()

# 🔄 Função que faz a troca de posição (i, j)
def swap_positions(rect_list, i, j):
    new_list = rect_list.copy()
    new_list[i], new_list[j] = new_list[j], new_list[i]
    return new_list

# ------------------------------
# Teste da função de troca
# ------------------------------

# Ordem inicial
current_order = rectangles

# Troca as posições que quiser (exemplo: troca posição 0 com 1)
new_order = swap_positions(current_order, 3, 5)

# Gera a solução com essa nova ordem
positions = shelf_first_fit_placement(new_order)

# Desenha o resultado
draw_solution(positions, title=f"Swap posições (0, 1)")

# ------------------------------
# Informações sobre a solução
# ------------------------------
area_container = CONTAINER_WIDTH * CONTAINER_HEIGHT
area_used = sum(w * h for (_, _, _, w, h) in positions)
area_wasted = area_container - area_used

print(f"Área usada: {area_used}")
print(f"Área desperdiçada: {area_wasted}")
print(f"Retângulos colocados: {len(positions)} de {len(rectangles)}")
