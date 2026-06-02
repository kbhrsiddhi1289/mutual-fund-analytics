import pandas as pd
import os

folder_path = "data/raw"

files = os.listdir(folder_path)

for file in files:

    if file.endswith(".csv"):

        path = os.path.join(folder_path, file)

        df = pd.read_csv(path)

        print("\n====================")
        print("FILE:", file)

        print("\nShape:")
        print(df.shape)

        print("\nData Types:")
        print(df.dtypes)

        print("\nHead:")
        print(df.head())

        # Missing values check
        print("\nMissing Values:")
        missing_values = df.isnull().sum()

        print(missing_values)