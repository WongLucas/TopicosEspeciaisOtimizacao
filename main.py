import random
from rpp_utils import (
    ler_instancia_ins2d,
    ff_strip_packing_itens,
    bf_strip_packing_itens,
    bottom_left_packing_itens,
    bottom_left_width_fixed,
    guillotine_packing_bins,
    skyline_packing
)
from rpp_plot import (
    plot_strips,
    plot_bottom_left_bins,
    plot_bottom_left_width_fixed,
    plot_guillotine_bins
)

instancia = ler_instancia_ins2d("SPP(Min_Height)/T6e.ins2D")
largura = instancia['W']
altura = instancia['H']

itens_desordenados = instancia['itens'].copy()
random.shuffle(itens_desordenados)

#ff_strips = ff_strip_packing_itens(largura, instancia['itens'])
ff_strips = ff_strip_packing_itens(largura, itens_desordenados)
plot_strips(ff_strips, largura)

#bf_strips = bf_strip_packing_itens(largura, instancia['itens'])
bf_strips = bf_strip_packing_itens(largura, itens_desordenados)
plot_strips(bf_strips, largura)

bins = bottom_left_packing_itens(largura, altura,itens_desordenados)
plot_bottom_left_bins(bins, largura, altura)

positions, altura_total = bottom_left_width_fixed(largura, itens_desordenados)
plot_bottom_left_width_fixed(itens_desordenados, positions, largura, altura_total)

bins_guilhotina = guillotine_packing_bins(largura, altura, itens_desordenados)
plot_guillotine_bins(bins_guilhotina, largura, altura)

positions, altura_total = skyline_packing(largura, itens_desordenados)
plot_bottom_left_width_fixed(itens_desordenados, positions, largura, altura_total)