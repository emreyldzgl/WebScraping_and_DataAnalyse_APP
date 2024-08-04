import pandas as pd
import os

directory = r'.\Masaüstü\WebScraping\file'

combined_df = pd.DataFrame()

for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        file_path = os.path.join(directory, filename)
        df = pd.read_csv(file_path)
        combined_df = pd.concat([combined_df, df], ignore_index=True)

combined_df.to_csv('full_data.csv', index=False)
