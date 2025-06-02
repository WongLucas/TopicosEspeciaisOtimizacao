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
    bins = []        # Lista de bins, cada bin é uma lista de (item, posição)
    itens_restantes = itens.copy()

    while itens_restantes:
        positions = []
        ocupados = []
        pontos_livres = [(0, 0)]

        itens_nao_cabem = []

        for item in itens_restantes:
            w, h = item['w'], item['h']
            melhor_ponto = None

            pontos_livres.sort(key=lambda p: (p[1], p[0]))

            for (px, py) in pontos_livres:
                if px + w > W or py + h > H:
                    continue

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
                itens_nao_cabem.append(item)
                continue  # tenta no próximo bin

            x, y = melhor_ponto
            positions.append({'item': item, 'pos': (x, y)})
            ocupados.append((x, y, w, h))

            pontos_livres.remove((x, y))
            novos_pontos = [
                (x + w, y),   # direita
                (x, y + h)    # acima
            ]
            for p in novos_pontos:
                if p not in pontos_livres:
                    pontos_livres.append(p)

        bins.append(positions)
        itens_restantes = itens_nao_cabem

    return bins


def bottom_left_width_fixed(W, itens):
    positions = []
    ocupados = []

    # Pontos livres iniciais
    pontos_livres = [(0, 0)]

    altura_total = 0

    for item in itens:
        w, h = item['w'], item['h']
        melhor_ponto = None

        # Ordena os pontos livres (menor y, depois menor x)
        pontos_livres.sort(key=lambda p: (p[1], p[0]))

        for (px, py) in pontos_livres:
            # Verifica se cabe na largura
            if px + w > W:
                continue

            # Não verifica altura, porque ela é livre (aumenta se necessário)

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
            # Se não encontrou, abre uma nova linha (em nova altura)
            nova_altura = altura_total
            melhor_ponto = (0, nova_altura)

        x, y = melhor_ponto
        positions.append((x, y))
        ocupados.append((x, y, w, h))

        # Atualiza altura total, se necessário
        altura_total = max(altura_total, y + h)

        # Atualiza pontos livres
        if (x + w, y) not in pontos_livres:
            pontos_livres.append((x + w, y))
        if (x, y + h) not in pontos_livres:
            pontos_livres.append((x, y + h))

        # Remove ponto usado
        if (x, y) in pontos_livres:
            pontos_livres.remove((x, y))

    return positions, altura_total

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

def plot_bottom_left_bins(bins, W, H):
    """
    Plota o resultado do bottom_left_packing_itens, que retorna uma lista de bins,
    onde cada bin é uma lista de {'item': item, 'pos': (x, y)}.
    """
    for bin_idx, bin_positions in enumerate(bins):
        fig, ax = plt.subplots(figsize=(10, 6))
        cores = {}
        for obj in bin_positions:
            item = obj['item']
            x, y = obj['pos']
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
        ax.set_title(f'Bottom-Left Packing - Bin {bin_idx+1}')
        plt.show()

def plot_bottom_left_width_fixed(itens, positions, W, altura_total):
    """
    Plota o resultado do bottom_left_width_fixed.
    """
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
    ax.set_ylim(0, altura_total)
    ax.set_xlabel('Largura')
    ax.set_ylabel('Altura utilizada')
    ax.set_title('Bottom-Left Strip Packing (largura fixa)')
    plt.show()

instancia = ler_instancia_ins2d("SPP(Min_Height)/T7e.ins2D")
largura = 100#instancia['W']

ff_strips = ff_strip_packing_itens(largura, instancia['itens'])
plot_strips(ff_strips, largura)

bf_strips = bf_strip_packing_itens(largura, instancia['itens'])
plot_strips(bf_strips, largura)

bins = bottom_left_packing_itens(largura, instancia['H'], instancia['itens'])
plot_bottom_left_bins(bins, largura, instancia['H'])

positions, altura_total = bottom_left_width_fixed(largura, instancia['itens'])
plot_bottom_left_width_fixed(instancia['itens'], positions, largura, altura_total)

