import requests
from tqdm import tqdm

base_url = "https://dadosabertos.camara.leg.br/arquivos/votacoesVotos/csv/votacoesVotos-{}.csv"

for year in tqdm(range(1987, 2024), desc="Downloading CSVs"):
    url = base_url.format(year)
    response = requests.get(url, stream=True)
    
    if response.status_code == 200:
        with open(f"./dados-coletados/votos-{year}.csv", "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
    else:
        print(f"Failed to download the CSV for year {year}. Status code: {response.status_code}")

print("Download completed!")
