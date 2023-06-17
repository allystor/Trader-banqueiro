import requests
import json


class DolarVsMundoAPI:
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