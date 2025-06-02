import matplotlib.pyplot as plt
import random

def ler_instancia_ins2d(caminho_arquivo):
    with open(caminho_arquivo, 'r') as f:
        linhas = [linha.strip() for linha in f if linha.strip() and not linha.startswith('#')]
    
    m = int(linhas[0])
    W, H = map(int, linhas[1].split())
    itens = []
    for linha in linhas[2:2 + m]:
        partes = linha.split()
        item = {
            'id': int(partes[0]),
            'w': int(partes[1]),
            'h': int(partes[2]),
            'd': int(partes[3]),
            'b': int(partes[4]),
            'p': int(partes[5])
        }
        itens.append(item)
    return {
        'm': m,
        'W': W,
        'H': H,
        'itens': itens
    }

def ff_strip_packing_itens(W, itens):
    strips = []

    for item in itens:
        colocado = False
        for strip in strips:
            largura_usada = sum(i['w'] for i in strip)
            if largura_usada + item['w'] <= W:
                strip.append(item)
                colocado = True
                break
        if not colocado:
            strips.append([item])
    return strips

def bf_strip_packing_itens(W, itens):
    strips = []  # Cada strip é um dicionário: {'altura': h, 'itens': [...]}

    for item in itens:
        melhor_strip = None
        menor_sobra = None
        for strip in strips:
            # Só considera strips onde o item cabe na altura
            if item['h'] <= strip['altura']:
                largura_usada = sum(i['w'] for i in strip['itens'])
                sobra = W - (largura_usada + item['w'])
                if sobra >= 0:
                    if (menor_sobra is None) or (sobra < menor_sobra):
                        menor_sobra = sobra
                        melhor_strip = strip
        if melhor_strip is not None:
            melhor_strip['itens'].append(item)
        else:
            # Cria nova strip com altura do item
            strips.append({'altura': item['h'], 'itens': [item]})

    # Para compatibilizar com a função de plotagem, retorna lista de listas de itens
    return [strip['itens'] for strip in strips]

def bottom_left_packing_itens(W, H, itens):
    positions = []
    ocupados = []

    # Pontos livres iniciais: (0, 0) é o canto inferior esquerdo
    pontos_livres = [(0, 0)]

    for item in itens:
        w, h = item['w'], item['h']
        melhor_ponto = None

        # Ordena os pontos livres por menor y, depois menor x
        pontos_livres.sort(key=lambda p: (p[1], p[0]))

        for (px, py) in pontos_livres:
            # Verifica se cabe no bin
            if px + w > W or py + h > H:
                continue

            # Verifica sobreposição
            sobrepoe = False
            for ox, oy, ow, oh in ocupados:
                if not (px + w <= ox or px >= ox + ow or
                        py + h <= oy or py >= oy + oh):
                    sobrepoe = True
                    break
            if not sobrepoe:
                melhor_ponto = (px, py)
                break

        if melhor_ponto is None:
            raise Exception("Não cabe no bin")

        x, y = melhor_ponto
        positions.append((x, y))
        ocupados.append((x, y, w, h))

        # Atualiza os pontos livres
        pontos_livres.remove((x, y))
        # Adiciona novos pontos: à direita e acima do retângulo colocado
        novos_pontos = [
            (x + w, y),   # ponto à direita
            (x, y + h)    # ponto acima
        ]
        for p in novos_pontos:
            if p not in pontos_livres:
                pontos_livres.append(p)

    return positions


def plot_strips(strips, W):
    fig, ax = plt.subplots(figsize=(10, 6))
    y_offset = 0
    cores = {}

    for idx, strip in enumerate(strips):
        x_offset = 0
        max_h = 0
        for item in strip:
            # Cor única por id
            if item['id'] not in cores:
                cores[item['id']] = (random.random(), random.random(), random.random())
            rect = plt.Rectangle((x_offset, y_offset), item['w'], item['h'],
                                 facecolor=cores[item['id']], edgecolor='black', alpha=0.7)
            ax.add_patch(rect)
            ax.text(x_offset + item['w']/2, y_offset + item['h']/2, str(item['id']),
                    ha='center', va='center', fontsize=8, color='black')
            x_offset += item['w']
            max_h = max(max_h, item['h'])
        y_offset += max_h

    ax.set_xlim(0, W)
    ax.set_ylim(0, y_offset)
    ax.set_xlabel('Largura')
    ax.set_ylabel('Altura acumulada')
    ax.set_title('Visualização do 2D Strip Packing')
    #plt.gca().invert_yaxis()
    plt.show()

def plot_bottom_left(itens, positions, W, H):
    fig, ax = plt.subplots(figsize=(10, 6))
    cores = {}

    for item, (x, y) in zip(itens, positions):
        # Cor única por id
        if item['id'] not in cores:
            cores[item['id']] = (random.random(), random.random(), random.random())
        rect = plt.Rectangle((x, y), item['w'], item['h'],
                             facecolor=cores[item['id']], edgecolor='black', alpha=0.7)
        ax.add_patch(rect)
        ax.text(x + item['w']/2, y + item['h']/2, str(item['id']),
                ha='center', va='center', fontsize=8, color='black')

    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.set_xlabel('Largura')
    ax.set_ylabel('Altura')
    ax.set_title('Visualização do Bottom-Left Packing')
    #plt.gca().invert_yaxis()
    plt.show()

instancia = ler_instancia_ins2d("SPP(Min_Height)/T5a.ins2D")

""" ff_strips = ff_strip_packing_itens(instancia['W'], instancia['itens'])
for idx, strip in enumerate(ff_strips):
    print(f"Strip {idx+1}: {[item['id'] for item in strip]}")

bf_strips = bf_strip_packing_itens(instancia['W'], instancia['itens'])
for idx, strip in enumerate(bf_strips):
    print(f"Strip {idx+1}: {[item['id'] for item in strip]}")

plot_strips(ff_strips, instancia['W'])
plot_strips(bf_strips, instancia['W'])
 """

positions = bottom_left_packing_itens(150, 150, instancia['itens'])
plot_bottom_left(instancia['itens'], positions, instancia['W'], instancia['H'])