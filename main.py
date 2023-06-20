from __future__ import print_function

import os.path
import time
import requests
import json
from api import DolarAPI
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1w8tJCkDibtj7d1lKi_iJV5wx9CgWHhGHYFPZoQov6J8'
SAMPLE_RANGE_NAME = 'Cotações!A3:p72'


def main():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret_16395904571-8cgbgkkd9gj0t2gvmgomlp15dbcgglnv.apps.googleusercontent.com.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    while True:
        try:
            service = build('sheets', 'v4', credentials=creds)

            # Call the Sheets API
            #ler valores do googlesheets
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId='1w8tJCkDibtj7d1lKi_iJV5wx9CgWHhGHYFPZoQov6J8',
                                        range='Cotações!A3:p72').execute()
            values = result.get('values', [])

            print(values)

            #adicionar ou editar valores no googlesheets
            api = DolarAPI()
            dolar_vs_mundo = api.obter_cotacoes()

            for item in dolar_vs_mundo:
                currency_pair = item[0]
                last_value = float(item[1])

                try:
                    # Verificar se o par de moedas está disponível na API
                    if currency_pair in values:
                        # Obter os dados atualizados usando a API AwesomeAPI
                        response = requests.get(f"https://economia.awesomeapi.com.br/last/USD-{currency_pair}/1")
                        response.raise_for_status()  # Lançar uma exceção para erros de solicitação HTTP

                        data = response.json()

                        if response.status_code == 200 and currency_pair in data:
                            current_value = float(data[currency_pair]['bid'])
                            variation = current_value - last_value
                            percent_variation = (variation / last_value) * 100

                            item.append(current_value)
                            item.append(variation)
                            item.append(percent_variation)

                            result = sheet.values().update(spreadsheetId='1w8tJCkDibtj7d1lKi_iJV5wx9CgWHhGHYFPZoQov6J8',
                                                           range='Cotações!B15', valueInputOption='USER_ENTERED',
                                                           body={'values': dolar_vs_mundo}).execute()
                        else:
                            item.extend(["N/A", "N/A", "N/A"])
                    else:
                        item.extend(["N/A", "N/A", "N/A"])

                except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
                    print(f"Erro ao obter dados do par {currency_pair}: {e}")
            time.sleep(10)
        except HttpError as err:
            print(err)


if __name__ == '__main__':
    main()
