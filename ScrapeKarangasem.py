# %%
import html5lib
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import numpy as np
import datetime

# %%
# masukkan alamat URL
url = 'http://infocorona.karangasemkab.go.id/peta-sebaran-kasus-covid-19-di-karangasem/'

# mulai otomasi browser menggunakan selenium
driver = webdriver.Firefox()
driver.get(url)

# dan tunggu hingga browser secara sempurna menampilkan map
wait = WebDriverWait(driver, 10)
wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'elementor-widget-wrap')))
print('Ready to scrape')

# driver.execute_script("window.scrollTo(0, 1080)")

# driver.implicitly_wait(1)

soupKarangasem = BeautifulSoup(driver.page_source, 'html5lib')

driver.close()

# %%
tabel = soupKarangasem.find('div', class_='elementor-text-editor elementor-clearfix')

# %%
contain = tabel.findAll('td')

# %%
headers = [i.text for i in contain[1:7]]
# headers

# %%
seqKecamatan = np.arange(9, len(contain)-8, 8)
seqODP = np.arange(10, len(contain)-8, 8)
seqPDP = np.arange(11, len(contain)-8, 8)
seqOTG = np.arange(12, len(contain)-8, 8)
seqKonfirmasiPositif = np.arange(13, len(contain)-8, 8)
seqSembuh = np.arange(14, len(contain)-8, 8)

Kecamatan = []
ODP = []
PDP = []
OTG = []
KonfirmasiPositif = []
Sembuh = []
# %%
for i in range(len(contain)):
    if i in seqKecamatan:
        Kecamatan.append(contain[i].text)
    elif i in seqODP:
        ODP.append(contain[i].text)
    elif i in seqPDP:
        PDP.append(contain[i].text)
    elif i in seqOTG:
        OTG.append(contain[i].text)
    elif i in seqKonfirmasiPositif:
        KonfirmasiPositif.append(contain[i].text)
    elif i in seqSembuh:
        Sembuh.append(contain[i].text)
        
# %%
dataKarangasem = [Kecamatan,
                  ODP,
                  PDP,
                  OTG,
                  KonfirmasiPositif,
                  Sembuh]

# %%
df = pd.DataFrame(dataKarangasem).transpose()
df.columns = headers
# df

# %%
now = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
TanggalWaktuScrape = [now for i in range(df.shape[0])]

# Tanggal = [str(datetime.date.today()) for i in range(df.shape[0])]
Kabupaten = ['Karangasem' for i in range(df.shape[0])]

# %%
df.insert(0, column='Tanggal Waktu Scrape', value=TanggalWaktuScrape)
df.insert(1, column='Kabupaten', value=Kabupaten)

SourceLink = [url for i in range(df.shape[0])]
df.insert(df.shape[1], column='Source Link', value=SourceLink)

# %%
print(df)

# %%
Tanggal = datetime.date.today()

df.to_csv(r'B:\Projects\Work\Covid-19\Data Scraping Bali\Karangasem_' + str(Tanggal) + '.csv')