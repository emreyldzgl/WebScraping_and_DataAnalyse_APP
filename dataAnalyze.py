import pandas as pd
import numpy as np
import ast

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.1f' % x)
pd.set_option('display.width', 500)

df = pd.read_csv("Full_Extract_Data.csv")
df.head()

def clean_genres(string_list):
    try:
        # String'i listeye dönüştür
        actual_list = ast.literal_eval(string_list)
        # Virgül ve boşluk karakterlerini içermeyen öğeleri sakla
        return [item.strip() for item in actual_list if item.strip() and item.strip() != ',']
    except:
        # Dönüşümde hata olursa boş liste döndür
        return []


df['Türler'] = df['Türler'].apply(clean_genres)
# Türler kolonunda bulunan tüm benzersiz türleri bul
all_genres = set(genre for sublist in df['Türler'] for genre in sublist)
# Her benzersiz tür için yeni bir kolon oluştur ve türün var olup olmadığını belirt
for genre in all_genres:
    df[genre] = df['Türler'].apply(lambda x: int(genre in x))
# Türler kolonunu kaldırabilirsiniz
df = df.drop(columns=['Türler'])

df['Yayınlanma Süresi'] = df['Basım Tarihi'] - df['İlk Yayın Tarihi']
df['Okuma/Begeni Oranı'] = df['Okunma Sayısı'] / df['Begeni Sayısı']

# Çevirmen Verilerinin Düzenlenmesi
df["Çevirmen"].value_counts()
# Çevirmen sütununda belirli anahtar kelimeleri içerenleri NaN ile değiştirme
keywords_to_replace = ['Derleyen', 'Yazar', 'Editör']
df['Çevirmen'] = df['Çevirmen'].apply(
    lambda x: np.nan if any(keyword in str(x) for keyword in keywords_to_replace) else x)

df.head()

df.to_excel("Ready_Data.xlsx", index=False)
