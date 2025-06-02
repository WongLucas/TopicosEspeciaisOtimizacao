import matplotlib.pyplot as plt
import random

def plot_strips(strips, W):
    fig, ax = plt.subplots(figsize=(10, 6))
    y_offset = 0
    cores = {}
    for idx, strip in enumerate(strips):
        x_offset = 0
        max_h = 0
        for item in strip:
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
    plt.show()

def plot_bottom_left_bins(bins, W, H):
    for bin_idx, bin_positions in enumerate(bins):
        fig, ax = plt.subplots(figsize=(10, 6))
        cores = {}
        for obj in bin_positions:
            item = obj['item']
            x, y = obj['pos']
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
    fig, ax = plt.subplots(figsize=(10, 6))
    cores = {}
    for item, (x, y) in zip(itens, positions):
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

def plot_guillotine_bins(bins, W, H):
    """
    Plota o resultado da heurística de corte guilhotinado para múltiplos bins.
    bins: lista de bins, cada bin é uma lista de {'item': item, 'pos': (x, y)}
    """
    import matplotlib.pyplot as plt
    import random

    for bin_idx, bin_positions in enumerate(bins):
        fig, ax = plt.subplots(figsize=(10, 6))
        cores = {}
        for obj in bin_positions:
            item = obj['item']
            pos = obj['pos']
            if pos is None:
                continue  # Não plota itens que não couberam
            x, y = pos
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
        ax.set_title(f'Guillotine Packing - Bin {bin_idx+1}')
        plt.show()