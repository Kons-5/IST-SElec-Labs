# Exemplo 2 (main_exemplo_2.py)
import T_Display
import math             # módulo de funções matemáticas

# Inicializações de variáveis globais
width = 160
height = 134

# Função para realizar amostras e médias
def media_amostras(num_amostras):
    # Apaga parte direita do display excepto icon WiFi
    tft.display_set(tft.BLACK, width, 0, 240-width, height-16)
    soma=0
    for n in range(num_amostras):
        pontos_adc = tft.read_adc(100, 50)   # 10 amostras num total de 50ms
        for j in range(100):
            soma += pontos_adc[j]
    media = soma / (100*num_amostras)

    # Escreve valores no display
    tft.display_write_str(tft.Arial16, "media", width +5, 90)
    tft.display_write_str(tft.Arial16, "%d" % num_amostras, width +5, 70)
    tft.display_write_str(tft.Arial16, "amostras", width +5, 50)
    tft.display_write_str(tft.Arial16, "%.2f" % media, width +5, 30)

# Programa principal (main)
tft = T_Display.TFT()                              # Instancia um objeto da classe TFT
tft.display_set(tft.BLACK, 0, 0, 240, 135)         # Apaga display
tft.display_write_grid(0, 0, 160, 135, 8, 8, True) # Desenha grelha (c/ linhas centrais)

frequencia = 50
amplitude = 3

# HORIZONTAL:
#   160 pixéis corresponde a 80ms (10ms por divisão) - Cada pixel 0.5ms
# VERTICAL:
#   134 pixéis corresponde a 8V (1V por divisão) - Cada volt (134/8) pixéis
x = []
y = []

# Desenha onda sinusoidal
for n in range(width):
    t = n * 0.0005
    volt = amplitude*math.sin(2*math.pi*frequencia*t)   # tensão em volt
    pixel = height/2 + (height/8)*volt
    x.append(n)
    y.append(round(pixel))
tft.display_nline(tft.YELLOW, x, y)
tft.set_wifi_icon(240-16,135-16)

while tft.working():                                    # Ciclo principal do programa
    but=tft.readButton()
    if but!=tft.NOTHING:
        print("Button pressed:",but)
        if but==11:                                     # Button 1 click (10 amostras)
            media_amostras(10)
        if but==21:                                     # Button 2 click (100 amostras)
            media_amostras(100)