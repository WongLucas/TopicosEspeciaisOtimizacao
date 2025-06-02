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
    return {'m': m, 'W': W, 'H': H, 'itens': itens}

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
    strips = []
    for item in itens:
        melhor_strip = None
        menor_sobra = None
        for strip in strips:
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
            strips.append({'altura': item['h'], 'itens': [item]})
    return [strip['itens'] for strip in strips]

def bottom_left_packing_itens(W, H, itens):
    bins = []
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
                    if not (px + w <= ox or px >= ox + ow or py + h <= oy or py >= oy + oh):
                        sobrepoe = True
                        break
                if not sobrepoe:
                    melhor_ponto = (px, py)
                    break
            if melhor_ponto is None:
                itens_nao_cabem.append(item)
                continue
            x, y = melhor_ponto
            positions.append({'item': item, 'pos': (x, y)})
            ocupados.append((x, y, w, h))
            pontos_livres.remove((x, y))
            novos_pontos = [(x + w, y), (x, y + h)]
            for p in novos_pontos:
                if p not in pontos_livres:
                    pontos_livres.append(p)
        bins.append(positions)
        itens_restantes = itens_nao_cabem
    return bins

def bottom_left_width_fixed(W, itens):
    positions = []
    ocupados = []
    pontos_livres = [(0, 0)]
    altura_total = 0
    for item in itens:
        w, h = item['w'], item['h']
        melhor_ponto = None
        pontos_livres.sort(key=lambda p: (p[1], p[0]))
        for (px, py) in pontos_livres:
            if px + w > W:
                continue
            sobrepoe = False
            for ox, oy, ow, oh in ocupados:
                if not (px + w <= ox or px >= ox + ow or py + h <= oy or py >= oy + oh):
                    sobrepoe = True
                    break
            if not sobrepoe:
                melhor_ponto = (px, py)
                break
        if melhor_ponto is None:
            nova_altura = altura_total
            melhor_ponto = (0, nova_altura)
        x, y = melhor_ponto
        positions.append((x, y))
        ocupados.append((x, y, w, h))
        altura_total = max(altura_total, y + h)
        if (x + w, y) not in pontos_livres:
            pontos_livres.append((x + w, y))
        if (x, y + h) not in pontos_livres:
            pontos_livres.append((x, y + h))
        if (x, y) in pontos_livres:
            pontos_livres.remove((x, y))
    return positions, altura_total

def guillotine_packing_bins(W, H, itens):
    itens_restantes = itens.copy()
    bins = []

    while itens_restantes:
        espacos_livres = [(0, 0, W, H)]
        bin_positions = []
        itens_nao_cabem = []

        for item in itens_restantes:
            melhor_espaco = None
            menor_sobra_area = None

            for idx, (ex, ey, ew, eh) in enumerate(espacos_livres):
                if item['w'] <= ew and item['h'] <= eh:
                    sobra_area = (ew * eh) - (item['w'] * item['h'])
                    if (menor_sobra_area is None) or (sobra_area < menor_sobra_area):
                        menor_sobra_area = sobra_area
                        melhor_espaco = (idx, ex, ey, ew, eh)

            if melhor_espaco is not None:
                idx, ex, ey, ew, eh = melhor_espaco
                bin_positions.append({'item': item, 'pos': (ex, ey)})

                # Remove espaço utilizado
                espacos_livres.pop(idx)

                # Calcula sobras para decidir como cortar
                sobra_direita = ew - item['w']
                sobra_cima = eh - item['h']

                # Escolhe o corte que maximiza a área dos subespaços
                if sobra_direita * eh >= ew * sobra_cima:
                    # Primeiro corta vertical (direita)
                    if sobra_direita > 0:
                        espacos_livres.append(
                            (ex + item['w'], ey, sobra_direita, eh)
                        )
                    if sobra_cima > 0:
                        espacos_livres.append(
                            (ex, ey + item['h'], item['w'], sobra_cima)
                        )
                else:
                    # Primeiro corta horizontal (acima)
                    if sobra_cima > 0:
                        espacos_livres.append(
                            (ex, ey + item['h'], ew, sobra_cima)
                        )
                    if sobra_direita > 0:
                        espacos_livres.append(
                            (ex + item['w'], ey, sobra_direita, item['h'])
                        )
            else:
                itens_nao_cabem.append(item)

        bins.append(bin_positions)
        itens_restantes = itens_nao_cabem

    return bins
