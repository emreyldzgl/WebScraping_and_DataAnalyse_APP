import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# WebDriver'ı başlat
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)


def extract_book_details(driver):
    """
    Kitap detaylarını sayfadan çeker.
    """
    try:
        kitaplar = driver.find_elements(By.XPATH, "//h1")
        kitap = [kitap.text for kitap in kitaplar]
    except Exception as e:
        print(f"Kitaplar bulunamadı: {e}")
        kitap = None

    try:
        yazarlar = driver.find_elements(By.XPATH,
                                        "//a[@class='text truncate text-15 text-mavi hover:underline self-start cursor']")
        yazar = [yazar.text for yazar in yazarlar]
    except Exception as e:
        print(f"Yazarlar bulunamadı: {e}")
        yazar = None

    try:
        puanmixler = driver.find_elements(By.XPATH,
                                          "//div[@class='dr flex-row'] //span[@class='text font-medium text-15']")
        puanmix = [puan.text for puan in puanmixler]
    except Exception as e:
        print(f"Puanlar bulunamadı: {e}")
        puanmix = None

    try:
        turler = driver.find_elements(By.XPATH,
                                      "//div[@class='dr flex-row mr-1']//span[@class='text text-mavi text-14']")
        turler = [tur.text for tur in turler]
    except Exception as e:
        print(f"Türler bulunamadı: {e}")
        turler = None

    try:
        datamixler = driver.find_elements(By.XPATH, "//span[@class='text text-14 mr-3']")
        datamix = [data.text for data in datamixler]
    except Exception as e:
        print(f"Datamix bulunamadı: {e}")
        datamix = None

    try:
        saticilar = driver.find_elements(By.XPATH, "//span[@class='text font-medium truncate text-12']")
        satici = [satici.text for satici in saticilar]
    except Exception as e:
        print(f"Satıcılar bulunamadı: {e}")
        satici = None

    try:
        fiyatlar = driver.find_elements(By.XPATH, "//span[@class='text font-medium truncate text-14']")
        fiyat = [fiyat.text for fiyat in fiyatlar]
    except Exception as e:
        print(f"Fiyatlar bulunamadı: {e}")
        fiyat = None

    try:
        maxokurcinsiyetler = driver.find_elements(By.XPATH, "//span[@class='text font-medium text-18']")
        maxokurc = [okur.text for okur in maxokurcinsiyetler]
    except Exception as e:
        print(f"MaxOkurCinsiyet bulunamadı: {e}")
        maxokurc = None

    try:
        maxokuryuzdeler = driver.find_elements(By.XPATH, "//span[@class='text font-medium text-12']")
        maxokury = [okur.text for okur in maxokuryuzdeler]
    except Exception as e:
        print(f"MaxOkurYüzde bulunamadı: {e}")
        maxokury = None

    try:
        cevirmenler = driver.find_elements(By.XPATH, "//div[@class='dr flex-row mr-2 items-center']")
        cevirmen = [cevirmen.text for cevirmen in cevirmenler]
    except Exception as e:
        print(f"Çevirmenler bulunamadı: {e}")
        cevirmen = None

    return kitap, yazar, puanmix, turler, datamix, satici, fiyat, maxokurc, maxokury, cevirmen


def scrape_book_pages(book_links):
    """
    Her bir kitap linki için detayları çeker ve sonuçları bir DataFrame'e kaydeder.
    """
    Feature1 = []
    Feature2 = []
    Feature3 = []
    Feature4 = []
    Feature5 = []
    Feature6 = []
    Feature7 = []
    Feature8 = []
    Feature9 = []
    Feature10 = []

    for link in book_links:
        print(f"Link açılıyor: {link}")
        driver.get(link)
        time.sleep(3)  # Sayfanın yüklenmesini bekleyin

        kitap, yazar, puanmix, turler, datamix, satici, fiyat, maxokurc, maxokury, cevirmen = extract_book_details(
            driver)

        Feature1.append(kitap)
        Feature2.append(yazar)
        Feature3.append(puanmix)
        Feature4.append(turler)
        Feature5.append(datamix)
        Feature6.append(satici)
        Feature7.append(fiyat)
        Feature8.append(maxokurc)
        Feature9.append(maxokury)
        Feature10.append(cevirmen)

    return pd.DataFrame({
        'Kitap Adı': Feature1,
        'Yazar': Feature2,
        'Puan': Feature3,
        'Türler': Feature4,
        'Datamix': Feature5,
        'Satici': Feature6,
        'Fiyat': Feature7,
        'MaxOkurCinsiyet': Feature8,
        'MaxOkurYüzde': Feature9,
        'Çevirmen': Feature10

    })


# Ana sayfa scraping kodu (önceden tanımlanmış)
base_url = "https://1000kitap.com/kitaplar/en-cok-okunanlar?hl=tr&sayfa="


def extract_data_from_page(driver):
    kitap_adi = []
    yazar_adi = []
    puan_okuma_deger = []
    kitap_link_deger = []

    kitaplar = driver.find_elements(By.XPATH, '//h3')
    yazarlar = driver.find_elements(By.XPATH, "//div[contains(@class, 'dr pv-1')]")
    puan_okumalar = driver.find_elements(By.XPATH,
                                         "//div[@class='dr flex-row flex-wrap']//span[@class='text text-silik text-14']")
    kitap_linkler = driver.find_elements(By.XPATH,
                                         "//div[@class='dr flex-1 min-w-40']//a[@class='dr self-start max-w-full flex-row cursor']")

    for kitap in kitaplar:
        kitap_adi.append(kitap.text)
    for yazar in yazarlar:
        yazar_adi.append(yazar.text)
    for puan_okuma in puan_okumalar:
        puan_okuma_deger.append(puan_okuma.text)
    for kitap_link in kitap_linkler:
        kitap_link_deger.append(kitap_link.get_attribute("href"))

    return kitap_adi, yazar_adi, puan_okuma_deger, kitap_link_deger


def modify_link(link):
    if "/hakkinda" not in link:
        return link.replace("?hl=tr", "/hakkinda?hl=tr")
    return link


def scrape_pages(start_page, end_page, wait_time=5):
    all_kitap_adi = []
    all_yazar_adi = []
    all_puan_okuma_deger = []
    all_kitap_link_deger = []

    for page in range(start_page, end_page + 1):
        print(f"Sayfa {page} işleniyor...")
        driver.get(f"{base_url}{page}")
        time.sleep(3)

        kitap_adi, yazar_adi, puan_okuma_deger, kitap_link_deger = extract_data_from_page(driver)
        kitap_link_deger = [modify_link(link) for link in kitap_link_deger]

        all_kitap_adi.extend(kitap_adi)
        all_yazar_adi.extend(yazar_adi)
        all_puan_okuma_deger.extend(puan_okuma_deger)
        all_kitap_link_deger.extend(kitap_link_deger)

        if page % 10 == 0:
            print(f"{page} sayfa işlendi, {wait_time} saniye bekleniyor...")
            time.sleep(wait_time)

    return all_kitap_adi, all_yazar_adi, all_puan_okuma_deger, all_kitap_link_deger


# Veri çekme işlemini başlat
start_page = 151
end_page = 278
kitap_adi, yazar_adi, puan_okuma_deger, kitap_link_deger = scrape_pages(start_page, end_page)

# Verileri DataFrame'e dönüştür
df = pd.DataFrame({
    'Kitap Adı': kitap_adi,
    'Yazar Adı': yazar_adi,
    'Puan ve Okuma': puan_okuma_deger,
    'Kitap Linki': kitap_link_deger
})

# Kitap sayfalarındaki detayları çek
book_details_df = scrape_book_pages(df['Kitap Linki'])

book_details_df.to_csv("data151-278.csv")

# Tarayıcıyı kapat
driver.quit()
