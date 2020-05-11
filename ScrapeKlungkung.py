# %%
import html5lib
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import numpy as np
import re
import datetime

# %%
# masukkan alamat URL
url = 'https://covid19.klungkungkab.go.id/'

# mulai otomasi browser menggunakan selenium
driver = webdriver.Firefox()
driver.get(url)

# xpath = '/html/body/div[6]/div/img'
xpath = '/html/body/div[5]/div'

# dan tunggu hingga browser secara sempurna menampilkan map
wait = WebDriverWait(driver, 20)
wait \
    .until(EC.visibility_of_all_elements_located((By.XPATH, xpath)))
print('Ready to scrape')

driver.find_element_by_xpath(xpath).click()

driver.implicitly_wait(1)

# driver.execute_script("window.scrollTo(0, 1080)")

soupKlungkung = BeautifulSoup(driver.page_source, 'html5lib')

driver.close()

# %%
KecRaw = []
seqKec = [13,20,27,34]
for i in seqKec:
    css_selector = ".et_pb_code_0 > div:nth-child(1) > h2:nth-child(" + str(i) + ")"
    KecRaw.append(soupKlungkung.select_one(css_selector).text)

idxKec = KecRaw[0].find(' ')
Kec = [KecRaw[i][idxKec+1:].capitalize() for i in range(len(KecRaw))]

# %%
tabel = soupKlungkung.findAll('div', class_='right-side-data')

# %%
headers = ['Tanggal Update',
           'Waktu Update',
           'Tanggal Waktu Scrape',
           'Kabupaten',
           'Kecamatan']
for i in tabel[0].findAll('th'):
    headers.append(i.text.title())
headers.insert(10, 'Source Link')

# %%
Kecamatan = []
Desa = []
Positif = []
DalRawat = []
Sembuh = []
Meninggal = []

for i, i_fill in enumerate(tabel):
    for j, j_fill in enumerate(i_fill.findAll('td')):
        seqDesa = np.arange(0, len(i_fill.findAll('td')), 5)
        seqPositif = np.arange(1, len(i_fill.findAll('td')), 5)
        seqDalRawat = np.arange(2, len(i_fill.findAll('td')), 5)
        seqSembuh = np.arange(3, len(i_fill.findAll('td')), 5)
        seqMeninggal = np.arange(4, len(i_fill.findAll('td')), 5)
        
        if j in seqDesa:
            Desa.append(j_fill.text)
            Kecamatan.append(Kec[i])
        elif j in seqPositif:
            Positif.append(j_fill.text)
        elif j in seqDalRawat:
            DalRawat.append(j_fill.text)
        elif j in seqSembuh:
            Sembuh.append(j_fill.text)
        elif j in seqMeninggal:
            Meninggal.append(j_fill.text)

# %%
css_selector_tanggalwaktu = '.et_pb_code_0 > div:nth-child(1) > h5:nth-child(3)'
TanggalWaktuRaw = soupKlungkung.select_one(css_selector_tanggalwaktu).text

idxTanggal = TanggalWaktuRaw.find('AL ')
idxWaktu = TanggalWaktuRaw.find('UL ')

Tanggal = TanggalWaktuRaw[idxTanggal+3:idxWaktu-4]
Waktu = TanggalWaktuRaw[idxWaktu+3:]

Tanggal = [Tanggal for i in range(len(Desa))]
Waktu = [Waktu for i in range(len(Desa))]

TanggalWaktuScrape = [str(datetime.date.today()) for i in range(len(Desa))]

Kabupaten = ['Klungkung' for i in range(len(Desa))]

SourceLink = [url for i in range(len(Desa))]

# %%
dataKlungkung = [Tanggal,
                 Waktu,
                 TanggalWaktuScrape,
                 Kabupaten,
                 Kecamatan,
                 Desa,
                 Positif,
                 DalRawat,
                 Sembuh,
                 Meninggal,
                 SourceLink]

# %%
df = pd.DataFrame(dataKlungkung).transpose()
df.columns = headers
df.head()

# %%
df.to_csv(r'B:\Projects\Work\Covid-19\Data Scraping Bali\Klungkung_' + Tanggal[0] + '.csv')
