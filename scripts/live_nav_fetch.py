import requests
import pandas as pd

funds = {
    "sbi_bluechip": 119551,
    "icici_bluechip": 120503,
    "nippon_largecap": 118632,
    "axis_bluechip": 119092,
    "kotak_bluechip": 120841
}

for fund_name, amfi_code in funds.items():

    url = f"https://api.mfapi.in/mf/{amfi_code}"

    response = requests.get(url)

    data = response.json()

    nav_data = data['data']

    df = pd.DataFrame(nav_data)

    file_name = f"data/raw/{fund_name}.csv"

    df.to_csv(file_name, index=False)

    print(f"{fund_name} data saved successfully")