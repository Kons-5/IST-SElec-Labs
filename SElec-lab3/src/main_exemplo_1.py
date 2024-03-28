# Exemplo 1 (main_exemplo_1.py)
import T_Display

# Inicializações
pontos_volt = [0.0]*240                           # Lista com 240 floats

# Função de leitura dos valores do ADC e representação no display
def read_and_display():
    pontos_adc = tft.read_adc(240, 200)           # Lê 240 pontos do ADC em 200ms
    Vmax=0
    Vmin=0
    Vmed=0
    for n in range(240):
        V = 0.00044028 * pontos_adc[n] + 0.091455 # Converte valor do ADC em Volt
        V = V - 1                                 # Tensão entrada de referência de 1V
        V = V / fator                             # Entra com o efeito do div. resistivo
        pontos_volt[n] = V
        if n==0:                                  # Caso seja o primeiro ponto
            Vmax = Vmin = Vmed = V
        else:
            Vmed += V
            if V>Vmax: Vmax=V
            if V<Vmin: Vmin=V
    Vmed /= 240                                   # Divide pelo número de amostras

    # Escreve os valores em strings com 2 casas decimais
    str1 = "Vmax = %.2f" % Vmax
    str2 = "Vmin = %.2f" % Vmin
    str3 = "Vmed = %.2f" % Vmed

    tft.display_set(tft.BLACK, 0, 0, 240, 135)    # Apaga display

    # Escreve as strings no display
    tft.display_write_str(tft.Arial16, str1, 10, 20+60)
    tft.display_write_str(tft.Arial16, str2, 10, 20+30)
    tft.display_write_str(tft.Arial16, str3, 10, 20)
    tft.set_wifi_icon(0,135-16)                   # Coloca o icon wifi no display

# Programa principal (main)
fator = 1/29.3                                    # Fator do divisor resistivo
tft = T_Display.TFT()                             # Instancia um objeto da classe TFT
read_and_display()                                # Função de leitura e representação

while tft.working():                              # Ciclo principal do programa
    but=tft.readButton()                          # Lê estado dos botões
    if but!=tft.NOTHING:
        print("Button pressed:",but)
        if but==11:                               # Button 1 click - Repete função
            read_and_display()
        if but==21:                               # Button 2 click - Envia mail
            tft.send_mail(0.2/240,pontos_volt,"Lista de 240 pontos em 0.2 segundos.",
                          "pvitor@kvl.pt")