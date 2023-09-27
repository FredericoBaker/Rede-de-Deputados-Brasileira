import requests
import pandas as pd
from tqdm import tqdm

url = "https://dadosabertos.camara.leg.br/api/v2/votacoes"

range = [2003, 2011, 2015, 2016, 2017, 2019, 2020, 2021]

for ano in tqdm(range, desc = "Processing years"):
    params = {
        'dataInicio': f'{ano}-01-01',
        'dataFim': f'{ano}-12-31',
        'ordem': 'ASC',
        'ordenarPor': 'dataHoraRegistro',
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
            print(f"Falha na página {params['pagina']} e ano {ano}. Status code: {response.status_code}")
            break

    df = pd.DataFrame(all_data)
    df.to_csv(f'./dados-coletados/votacoes-{ano}.csv', index=False)

    print(f"Ano {ano} coletado.")