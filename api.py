import requests
import json


class DolarAPI:
    def __init__(self):
        # Lista de pares de moedas que você deseja obter cotações
        self.currency_pairs = [
            "USDCHF", "USDCZK", "USDDKK", "USDEUR", "USDGBP", "USDHUF", "USDNOK", "USDSEK",
            "USDEGP", "USDNGN", "USDZAR", "USDCNY", "USDHKD", "USDILS", "USDIDR", "USDINR",
            "USDJPY", "USDKRW", "USDMYR", "USDPHP", "USDRUB", "USDSAR", "USDSGD", "USDTRY",
            "USDTWD", "USDAUD", "USDNZD"
        ]

        # URL da API para obter os dados de cotação
        self.url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.10813/dados?formato=json"

    def obter_cotacoes(self):
        response = requests.get(self.url)
        data = response.json()

        cotacoes = []

        for item in data:
            data_cotacao = item["data"]
            valor_cotacao = item["valor"]

            # Verifica se o nome do par de moedas existe na lista currency_pairs
            if len(cotacoes) < len(self.currency_pairs):
                cotacoes.append([self.currency_pairs[len(cotacoes)], valor_cotacao])

        return cotacoes

class DolarAPI:
    def __init__(self):
        self.url = "https://api.exchangerate-api.com/v4/latest/USD"

    def get_dolar_data(self):
        response = requests.get(self.url)
        data = response.json()
        return data

    def get_dolar_min_max(self):
        data = self.get_dolar_data()
        rates = data["rates"]
        brl_rate = rates["BRL"]

        # Primeiro momento
        min1 = rates["BRL_min1"]
        max1 = rates["BRL_max1"]

        # Segundo momento
        min2 = rates["BRL_min2"]
        max2 = rates["BRL_max2"]

        # Terceiro momento
        min3 = rates["BRL_min3"]
        max3 = rates["BRL_max3"]

        return {
            "primeira": {"Máxima": max1, "Mínima": min1},
            "segunda": {"Máxima": max2, "Mínima": min2},
            "terceira": {"Máxima": max3, "Mínima": min3}
        }

def main():
    dolar_api = DolarAPI()
    dolar_min_max = dolar_api.get_dolar_min_max()

    print("    Máxima      Mínima")
    for momento, valores in dolar_min_max.items():
        maxima = valores["Máxima"]
        minima = valores["Mínima"]
        print(f"{momento}     {maxima}     {minima}")

if __name__ == '__main__':
    main()