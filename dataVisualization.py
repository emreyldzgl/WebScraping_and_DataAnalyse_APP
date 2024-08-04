import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import base64

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.1f' % x)
pd.set_option('display.width', 500)

df = pd.read_csv("dataset/Full_Extract_Data.csv")
df.head()


def extract_unique_genres(dataframe, column_name):
    # Türler sütununu listelere dönüştürme
    dataframe[column_name] = dataframe[column_name].apply(lambda x: eval(x) if isinstance(x, str) else x)
    # Tüm türleri içeren bir liste oluştur
    all_genres = [genre for sublist in dataframe[column_name] for genre in sublist]
    # Benzersiz türleri bul
    unique_genres = list(set(all_genres))
    # Listeyi virgülle ayırarak döndür
    return ', '.join(unique_genres)


def filter_by_genres(dataframe, genres_to_include):
    """
    Bu fonksiyon, belirtilen türleri içeren satırları seçip yeni bir DataFrame döndürür.

    :param dataframe: Veri çerçevesi (DataFrame)
    :param genres_to_include: İçerilmesini istediğiniz türlerin listesi
    :return: Türleri içeren yeni veri çerçevesi (DataFrame)
    """
    # Verinin 'Türler' sütunundaki liste formatındaki türleri kontrol ederek filtreleme yapıyoruz
    filtered_df = dataframe[dataframe['Türler'].apply(lambda x: all(genre in x for genre in genres_to_include))]
    return filtered_df


def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()



img = get_img_as_base64("images/background.png")
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
    background-image: url("data:image/png;base64,{img}");
    background-size: cover;
    background-position: center;
}}
[data-testid="stFullScreenFrame"] > .main {{
    background-image: url("data:image/png;base64,{img}");
    background-size: cover;
    background-position: center;
}}
[data-testid="stHeader"]
{{background: rgba(0,0,0,0.3);}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)


st.markdown("""
    <style>
    .title-center {
        text-align: center;
        font-size: 36px;
        font-weight: bold;
        color: black;
    }
    </style>
    """, unsafe_allow_html=True)
st.markdown('<p class="title-center"> ☕︎ Kitapların Türlerine Göre Veri Analizi 🕮</p>', unsafe_allow_html=True)
unique_genres = extract_unique_genres(df, 'Türler')
options = ["Psikoloji", "Eğlence-Mizah", "Diğer İnançlar", "Dilbilimi-Etimoloji", "Spor", "Halk Edebiyatı",
           "Özlü Sözler-Duvar Yazıları", "Gençlik", "Roman", "Şiir", "Edebiyat", "Antropoloji-Etnoloji", "Müzik",
           "Polisiye", "Efsaneler-Destanlar", "Eğitim", "Tasavvuf-Mezhepler-Tarikatlar", "Macera-Aksiyon", "Kültür",
           "Korku-Gerilim", "Hukuk", "Masal", "Manga", "Sosyoloji", "Mitolojiler", "Kadın-Erkek", "Dünya Klasikleri",
           "Söyleşi-Röportaj", "Tiyatro", "Sağlık-Tıp", "Din (İslam)", "Novella", "Kişisel Gelişim", "Antoloji",
           "Bilim-Teknoloji-Mühendislik", "Aile (Kadın, Erkek ve Çocuk)", "Aşk", "Türk Klasikleri", "Anlatı",
           "Sözlük-Kılavuz Kitap-Ansiklopedi", "İletişim-Medya", "Bilim-Kurgu", "Siyaset-Politika",
           "Ekonomi-Emek-İş Dünyası", "Senaryo-Oyun", "Araştırma-İnceleme", "Felsefe-Düşünce", "Deneme-İnceleme",
           "Sanat", "Ekoloji", "Fantastik", "Kadın", "Sinema", "Biyografi", "Gezi", "Tarih", "Yeraltı Edebiyatı",
           "Parapsikoloji-Spiritüalizm", "Çizgi-Roman", "Anı-Mektup-Günlük", "İnsan ve Toplum", "Eleştiri-Kuram",
           "Hikaye (Öykü)", "Çocuk"]
selected_turler = st.multiselect("", options, placeholder='Kitap Türü Seçiniz')

df_filter = filter_by_genres(df, selected_turler)

df_sort_value = df_filter.sort_values(by='Begeni Sayısı', ascending=False)

# Grafik oluşturma
fig, ax = plt.subplots(figsize=(12, 8))
sns.barplot(x='Begeni Sayısı', y='Kitap Adı', data=df_sort_value.head(10), color="darkred")
plt.title(f'{selected_turler} Türündeki En Çok Beğenilen 10 Kitap', fontsize=20, fontweight='bold')
plt.xlabel('Beğeni Sayısı', fontsize=20, fontweight='bold')
plt.ylabel('Kitap Adı', fontsize=20, fontweight='bold')

ax.tick_params(axis='both', which='major', labelsize=20)

fig.patch.set_facecolor('none')
ax.patch.set_facecolor('none')

st.pyplot(plt.gcf())

st.write(df_filter)


def remove_outliers_iqr(dataframe, column):
    Q1 = dataframe[column].quantile(0.25)
    Q3 = dataframe[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return dataframe[(dataframe[column] >= lower_bound) & (dataframe[column] <= upper_bound)]


st.markdown("""
    <style>
    .big-font {
        font-size: 28px !important;
        color: black; 
        font-weight: bold; 
    }
    </style>
    """, unsafe_allow_html=True)
st.markdown('<p class="big-font">Seçilen Tür/Türlere Göre Kitap Puanları ve Sayfa Sayısı</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

if col1.button('ScatterpLot'):
    # Sayfa Sayısı ve Puan sütunları için outlier'ları kaldırma
    df_no_outliers = remove_outliers_iqr(df_filter, 'Sayfa Sayısı')
    df_no_outliers = remove_outliers_iqr(df_no_outliers, 'Puan')

    # Grafik oluşturma
    fig, ax = plt.subplots(figsize=(6, 5))

    # Scatter plot
    sns.scatterplot(x='Sayfa Sayısı', y='Puan', data=df_no_outliers, hue='Puan', color="red", s=100,
                    alpha=0.7)
    plt.xlabel('Beğeni Sayısı', fontsize=14, fontweight='bold')
    plt.ylabel('Kitap Adı', fontsize=14, fontweight='bold')
    # Yoğunluk çizgisi
    sns.kdeplot(x='Sayfa Sayısı', y='Puan', data=df_no_outliers, color="red", fill=True, alpha=0.3)

    plt.title(f'Türler : {selected_turler}')
    plt.xlabel('Sayfa Sayısı')
    plt.ylabel('Puan')
    plt.legend(title='Puan')

    fig.patch.set_facecolor('none')
    ax.patch.set_facecolor('none')

    st.pyplot(plt.gcf())

if col2.button('Lineplot'):
    df_no_outliers = remove_outliers_iqr(df_filter, 'Sayfa Sayısı')
    df_no_outliers = remove_outliers_iqr(df_no_outliers, 'Puan')

    # Sayfa Sayısını aralıklara ayırma
    bins = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, ]

    labels = ['50-100', '100-150', '150-200', '200-250', '250-300', '300-350', '350-400',
              '400-450', '450-500', '500-550', '550-600', '600-650', '650-700', '700-750', '750-800']

    df_no_outliers['Sayfa Sayısı Aralığı'] = pd.cut(df_no_outliers['Sayfa Sayısı'], bins=bins, labels=labels,
                                                    right=False)

    # Her aralık için puan ortalamasını hesaplama
    mean_scores = df_no_outliers.groupby('Sayfa Sayısı Aralığı')['Puan'].mean().reset_index()

    # Grafik oluşturma
    fig, ax = plt.subplots(figsize=(6, 5))

    # Çizgi grafiği
    sns.lineplot(x='Sayfa Sayısı Aralığı', y='Puan', data=mean_scores, marker='o', ax=ax, color="red")

    # Grafik başlığı ve etiketler
    ax.set_title('Sayfa Sayısı Aralıklarına Göre Ortalama Puanlar')
    ax.set_xlabel('Sayfa Sayısı Aralığı')
    ax.set_ylabel('Ortalama Puan')

    fig.patch.set_facecolor('none')
    ax.patch.set_facecolor('none')
    # X eksenindeki etiketleri döndürme
    plt.xticks(rotation=45, ha='right')

    st.pyplot(plt.gcf())

st.markdown('<p class="big-font">Seçilen Tür/Türlere Göre Okuyucuların Yüzdeleri</p>', unsafe_allow_html=True)
if st.button("Pie Graph"):

    # Sayfa Sayısı ve Puan sütunları için outlier'ları kaldırma
    df_no_outliers = remove_outliers_iqr(df_filter, 'Erkek')
    df_no_outliers = remove_outliers_iqr(df_no_outliers, 'Kadın')

    # Cinsiyet yüzdelerini hesaplama
    erkek_yuzde = df_no_outliers['Erkek'].mean()
    kadin_yuzde = df_no_outliers['Kadın'].mean()

    # Pasta grafiği oluşturma
    # Pasta grafiği oluşturma
    fig, ax = plt.subplots(figsize=(6, 5))

    # Kenarlık ve gölge ekleme
    wedges, texts, autotexts = ax.pie(
        [erkek_yuzde, kadin_yuzde],
        labels=['Erkek', 'Kadın'],
        autopct='%1.1f%%',
        startangle=140,
        colors=["grey", "darkred"],
        wedgeprops=dict(width=0.3, edgecolor='w', linewidth=2),
        shadow=True
    )

    # Metinlerin stilini ayarlama
    for text in texts:
        text.set_color('grey')
        text.set_fontsize(12)
    for autotext in autotexts:
        autotext.set_color('black')
        autotext.set_fontsize(12)
        autotext.set_weight('bold')
    plt.title(f'Türler: {", ".join(selected_turler)} için Cinsiyet Yüzdeleri')

    ax.legend(wedges, ['Erkek', 'Kadın'], title="Cinsiyet", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

    fig.patch.set_facecolor('none')
    ax.patch.set_facecolor('none')

    st.pyplot(plt.gcf())
