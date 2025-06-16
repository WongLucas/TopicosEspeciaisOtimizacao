import random
from rpp_utils import (
    ler_instancia_ins2d,
    ff_strip_packing_itens,
    bf_strip_packing_itens,
    bottom_left_packing_itens,
    bottom_left_width_fixed,
    guillotine_packing_bins,
    skyline_packing,
    simulated_annealing_strip_packing
)
from rpp_plot import (
    plot_strips,
    plot_bottom_left_bins,
    plot_bottom_left_width_fixed,
    plot_guillotine_bins
)

instancia = ler_instancia_ins2d("SPP(Min_Height)/N1a.ins2D")
largura = instancia['W']
altura = instancia['H']

itens_desordenados = instancia['itens'].copy()
#random.shuffle(itens_desordenados)

#ff_strips = ff_strip_packing_itens(largura, instancia['itens'])
ff_strips, area_desperdicada = ff_strip_packing_itens(largura, altura, itens_desordenados)
plot_strips(ff_strips, largura, altura)

#bf_strips = bf_strip_packing_itens(largura, instancia['itens'])
bf_strips, area_desperdicada = bf_strip_packing_itens(largura, altura, itens_desordenados)
plot_strips(bf_strips, largura, altura)

# Para FF:
melhor_strips, melhor_desperdicio, desperdicio = simulated_annealing_strip_packing(
    instancia['itens'], instancia['W'], instancia['H'], ff_strip_packing_itens, log_file = "historico_ff.txt"
)
plot_strips(melhor_strips, largura, altura)

# Para BF:
melhor_strips, melhor_desperdicio, desperdicio = simulated_annealing_strip_packing(
    instancia['itens'], instancia['W'], instancia['H'], bf_strip_packing_itens, log_file = "historico_bf.txt"
)
plot_strips(melhor_strips, largura, altura)