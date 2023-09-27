import requests
import pandas as pd

url = "https://dadosabertos.camara.leg.br/api/v2/deputados"
params = {
    'dataInicio': '1991-01-01',
    'dataFim': '2024-01-01',
    'ordem': 'ASC',
    'ordenarPor': 'idLegislatura',
    'pagina': 1
}

all_data = []

while True:
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()

        if not data['dados']:
            # Caso em que não há mais dados
            break

        all_data.extend(data['dados'])

        # Incrementa o número da página para o próximo request
        params['pagina'] += 1

    else:
        print(f"Falha na página {params['pagina']}. Status code: {response.status_code}")
        break

df = pd.DataFrame(all_data)
df.to_csv('./dados-coletados/deputados.csv', index=False)

print("Dados salvos em dados-coletados/deputados.csv")