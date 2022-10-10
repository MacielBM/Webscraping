import requests
from bs4 import BeautifulSoup
import locale
from tabulate import tabulate
from modelos import FundoImobiliario, Estrategia

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


def trata_porcentagem(porcentagem_str):
    return locale.atof(porcentagem_str.split('%')[0])


def trata_decimal(decimal_str):
    return locale.atof(decimal_str)


headers = {'User-Agent': 'Mozilla/5.0'}
resposta = requests.post("https://www.fundamentus.com.br/fii_resultado.php", headers=headers)

soup = BeautifulSoup(resposta.text, 'html.parser')
linhas = soup.find(id="tabelaResultado").find('tbody').find_all('tr')
resultados = []
estrategia = Estrategia(
    cotacao_atual_minima=float(input("Qual a cotação Minima:R$ ")),
    dividend_yield_minimo=float(input("Qual o dividend Yield Minimo: ")),
    p_pv_minimo=float(input("Qual o pv minomo em % (ex: 0.7 ): ")),
    valor_mercado_minimo=float(input("Valor de mercado minimo:R$ ")),
    liquidez_minimo=float(input("Lidiquidez minima:R$ ")),
    qt_imoveis_minimo=int(input("Quantos Imoveis: ")),
    maxima_vacancia_media=float(input("Vacancia maxima: "))


)
for linha in linhas:
    dados_fundo = linha.find_all('td')

    codigo = dados_fundo[0].text
    segmento = dados_fundo[1].text
    cotacao = trata_decimal(dados_fundo[2].text)
    ffo_yield = trata_porcentagem(dados_fundo[3].text)
    dividend_yield = trata_porcentagem(dados_fundo[4].text)
    p_vp = trata_decimal(dados_fundo[5].text)
    valor_mercado = trata_decimal(dados_fundo[6].text)
    liquidez = trata_decimal(dados_fundo[7].text)
    qt_imoveis = int(dados_fundo[8].text)
    preco_m2 = trata_decimal(dados_fundo[9].text)
    aluguel_m2 = trata_decimal(dados_fundo[10].text)
    cap_rate = trata_porcentagem(dados_fundo[11].text)
    vacancia = trata_porcentagem(dados_fundo[12].text)

    fundo_imobiliario = FundoImobiliario(
        codigo, segmento, cotacao, ffo_yield, dividend_yield, p_vp, valor_mercado, liquidez,
        qt_imoveis, preco_m2, aluguel_m2, cap_rate, vacancia
    )

    if estrategia.aplica_estrategia(fundo_imobiliario):
        resultados.append(fundo_imobiliario)
cabecalho = ["Código", "Segmento", "Cotação Atual", "Dividend"]
tabela = []
for elemento in resultados:
    tabela.append([elemento.codigo, elemento.segmento, locale.currency(elemento.cota_atual), elemento.dividend_yield])

print(tabulate(tabela, showindex="always", tablefmt="fancy_grid"))
# print(
#     f'\n\nCode:{dados_fundo[0].text}\n'
#     f'\tCotação: {dados_fundo[2].text}\n'
#     f'\tSetor: {dados_fundo[1].text}\n'
#     f'\tDY %: {dados_fundo[4].text}\n'
#     f'\tP/VP: {dados_fundo[5].text}'
# )
