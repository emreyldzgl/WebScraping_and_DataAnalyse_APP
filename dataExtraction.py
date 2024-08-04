import pandas as pd
import numpy as np
import ast
import re

df = pd.read_csv("full_data.csv")
df.head()

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.1f' % x)
pd.set_option('display.width', 500)

df.head()
df.tail()
df.shape
# (4986, 11)

filtered_df = df[df["Kitap Adı"].apply(lambda x: "Kitap bulunamadı" not in x)]

filtered_df.shape
# (4164, 11)

df = filtered_df

df = df.drop(columns=["Unnamed: 0"])

df["Kitap Adı"] = df["Kitap Adı"].str.replace(r"[\'\[\]]", "", regex=True)
df["Yazar"] = df["Yazar"].str.replace(r"[\'\[\]]", "", regex=True)
df["Çevirmen"] = df["Çevirmen"].str.replace(r"[\'\[\]]", "", regex=True)
df["MaxOkurCinsiyet"] = df["MaxOkurCinsiyet"].str.replace(r"[\'\[\]]", "", regex=True)

df.head()


df["Puan"] = df["Puan"].str.replace(r"[\'\[\]]", "", regex=True)
df[['Puan', 'Okunma Sayısı', 'Begeni Sayısı']] = df["Puan"].str.split(' ', expand=True)
df["Puan"] = df["Puan"].str.split('/', expand=True)[0]

# Eksik Değerlerin Çıkarılması
df.isna().sum()
df = df.dropna()

df['Puan'] = pd.to_numeric(df['Puan'], errors='coerce')


df["Okunma Sayısı"] = df["Okunma Sayısı"].str.rstrip(',')


def convert_to_numeric(value):
    if pd.isna(value):  # None veya NaN durumunu kontrol et
        return None

    if 'bin' in value:
        value = value.replace('bin', '')
        return int(float(value.replace('.', '').replace(',', '.')) * 1000)
    else:
        return int(value.replace('.', '').replace(',', ''))




df['Okunma Sayısı'] = df['Okunma Sayısı'].apply(convert_to_numeric)
df['Okunma Sayısı'] = df['Okunma Sayısı'].astype(int)

df['Begeni Sayısı'] = df['Begeni Sayısı'].apply(convert_to_numeric)
df['Begeni Sayısı'] = df['Begeni Sayısı'].astype(int)

df.head()

# String listeleri gerçek listelere dönüştürme ve temizleme işlemi
def clean_genres(string_list):
    try:
        # String'i listeye dönüştür
        actual_list = ast.literal_eval(string_list)
        # Virgül ve boşluk karakterlerini içermeyen öğeleri sakla
        return [item.strip() for item in actual_list if item.strip() and item.strip() != ',']
    except:
        # Dönüşümde hata olursa boş liste döndür
        return []


# Döngü ile tüm öğeleri işleme
df['Türler'] = df['Türler'].apply(clean_genres)
df['Satici'] = df['Satici'].apply(clean_genres)
df['Fiyat'] = df['Fiyat'].apply(clean_genres)
df['MaxOkurYüzde'] = df['MaxOkurYüzde'].apply(clean_genres)



# Fiyat sütununu iki ayrı sütuna bölme
df[['Bkmkitap', 'Kitapyurdu']] = pd.DataFrame(df['Fiyat'].tolist(), index=df.index)
df = df.drop(columns=["Satici", "Fiyat"])

def to_float(value):
    # Eğer değer None ise, None olarak bırakın
    if pd.isna(value):
        return None
    # ₺ sembolünü ve virgülleri kaldırın, noktaya dönüştürün ve float türüne dönüştürün
    value = value.replace('₺', '').replace(',', '.')
    return float(value)


df['Bkmkitap'] = df['Bkmkitap'].apply(to_float)
df['Kitapyurdu'] = df['Kitapyurdu'].apply(to_float)


# Liste içindeki yüzdeleri float olarak dönüştürme
def extract_percentage(value):
    if isinstance(value, list) and value:
        # Listenin ilk elemanını al ve % ile boşlukları temizle
        percentage_str = value[0].replace('%', '').strip()
        try:
            # String'i float'a çevir
            return float(percentage_str)
        except ValueError:
            # Eğer float'a dönüşemiyorsa NaN döndür
            return None
    return None


# Fonksiyonu apply ile tüm sütuna uygula
df['MaxOkurYüzde'] = df['MaxOkurYüzde'].apply(extract_percentage)


# Yeni sütunları oluşturma
df['Erkek'] = df.apply(lambda row: row['MaxOkurYüzde'] if row['MaxOkurCinsiyet'] == 'Erkek' else 100 - row['MaxOkurYüzde'], axis=1)
df['Kadın'] = df.apply(lambda row: row['MaxOkurYüzde'] if row['MaxOkurCinsiyet'] == 'Kadın' else 100 - row['MaxOkurYüzde'], axis=1)

df = df.drop(columns=["MaxOkurYüzde", "MaxOkurCinsiyet"])

df.head()


df['Datamix_dict'] = None
# Her satır için döngü
for index, row in df.iterrows():
    # Datamix sütunundaki veriyi alın
    veri = row['Datamix']
    # Veriyi listeye dönüştürün
    ogeler = ast.literal_eval(veri)
    # Veriyi bir sözlük yapısına dönüştürmek için boş bir sözlük oluşturun
    veri_sozluk = {}
    # Her bir öğeyi key-value çiftlerine ayırın ve sözlüğe ekleyin
    for oge in ogeler:
        key, value = oge.split(": ", 1)  # ': ' dan sadece ilk gördüğünde split yapacak
        veri_sozluk[key] = value
    # Sözlüğü yeni sütuna ekleyin
    df.at[index, 'Datamix_dict'] = veri_sozluk

# Yeni sütunlar oluşturmak için döngü
for index, row in df.iterrows():
    # Datamix_dict sütunundaki sözlük veriyi alın
    datamix_dict = df.at[index, 'Datamix_dict']
    # Sözlükteki her bir anahtar-değer çifti için
    for key, value in datamix_dict.items():
        # Eğer sütun mevcut değilse oluşturun
        if key not in df.columns:
            df[key] = None
        # Değeri sütuna ekleyin
        df.at[index, key] = value


df = df.drop(columns=["Datamix", "Datamix_dict", "Orijinal Adı"])


# Her satır için döngü
for index, row in df.iterrows():
    # Çevirmen sütunundaki veriyi alın
    veri = row['Çevirmen']

    # Veriyi ayırmak için regex kullanarak key-value çiftlerini bulun
    key_value_pairs = re.findall(r'(\w+):\s*\\n(.*?)(?=,|$)', veri)

    # Her bir anahtar-değer çifti için döngü
    for key, value in key_value_pairs:
        # Eğer sütun mevcut değilse oluşturun
        if key not in df.columns:
            df[key] = None

        # Değeri sütuna ekleyin
        df.at[index, key] = value.strip()

# 'Çevirmen' sütununda 'Yazar' ile başlayan satırları None olarak ayarlayın
df.loc[df['Çevirmen'].str.contains(r'^Yazar', na=False), 'Çevirmen'] = None


def convert_to_minutes(time_str):
    if pd.isna(time_str):
        return np.nan
    import re
    match = re.search(r'(?:(\d+)\s*sa\.|(\d+)\s*hrs\.)?\s*(?:(\d+)\s*dk\.|(\d+)\s*min\.)?', time_str)
    if not match:
        return np.nan
    hours_turkish = match.group(1)
    hours_english = match.group(2)
    minutes_turkish = match.group(3)
    minutes_english = match.group(4)
    total_minutes = 0
    if hours_turkish:
        total_minutes += int(hours_turkish) * 60
    if hours_english:
        total_minutes += int(hours_english) * 60
    if minutes_turkish:
        total_minutes += int(minutes_turkish)
    if minutes_english:
        total_minutes += int(minutes_english)
    return total_minutes


# Tahmini Okuma Süresi sütununu dönüştür
df['Tahmini Okuma Süresi'] = df['Tahmini Okuma Süresi'].apply(convert_to_minutes)
df['Tahmini Okuma Süresi'] = df['Tahmini Okuma Süresi'].replace('', np.nan).astype(float).fillna(0).astype(int)

# Basım Tarihi sütununu sadece yıl olarak al
df['Basım Tarihi'] = df['Basım Tarihi'].str[-4:]
df['Basım Tarihi'] = df['Basım Tarihi'].replace('', np.nan).astype(float).fillna(0).astype(int)

# İlk Yayın Tarihi sütununu yıl olarak dönüştür
df['İlk Yayın Tarihi'] = df['İlk Yayın Tarihi'].str[-4:]
df['İlk Yayın Tarihi'] = df['İlk Yayın Tarihi'].replace('', np.nan).astype(float).fillna(0).astype(int)

# Sayfa Sayısı sütununu dönüştür
df['Sayfa Sayısı'] = df['Sayfa Sayısı'].replace('None', np.nan).astype(float).fillna(0).astype(int)


df.head()

df.to_csv("Full_Extract_Data.csv", index=False)
