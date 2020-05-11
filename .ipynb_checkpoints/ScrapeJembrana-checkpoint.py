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
url = 'https://covid19.jembranakab.go.id'

# mulai otomasi browser menggunakan selenium
driver = webdriver.Firefox()
driver.get(url)

# dan tunggu hingga browser secara sempurna menampilkan tabel yang diinginkan
wait = WebDriverWait(driver, 10)
wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "container")))
print('Ready to scrape')

driver.execute_script("window.scrollTo(0, 1080)")

driver.implicitly_wait(1)

soupJembrana = BeautifulSoup(driver.page_source, 'html5lib')

# %%
Kecamatan_temp = []
seqKecamatan = np.arange(0, 25, 5)
for i, i_fill in enumerate(soupJembrana.findAll('div', class_='table-responsive')):
    isi = i_fill.find('table',class_='table table-striped mx-auto w-auto') \
            .find('tbody').findAll('td')
    for j, j_fill in enumerate(isi):
        if i == 0 and j in seqKecamatan:
            Kecamatan_temp.append(j_fill.text)

# %%
# Kecamatan_temp

# %%
dataJembrana = []
headers = []

xpath = '//a[@class="btn btn-danger"]'
kliks = driver.find_elements_by_xpath(xpath)

action = webdriver.common.action_chains.ActionChains(driver)
action.move_by_offset(100, 0) #move 100 pixels to the right to close the popup window

seqButton = np.arange(1, len(kliks)+1)
    
# %%
for klik in range(len(kliks)):
    
    cssClick = 'div.row:nth-child(5) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(' + str(seqButton[klik]) + ') > td:nth-child(5) > a:nth-child(1)'
    
    element = driver.find_element_by_css_selector(cssClick)
    driver.execute_script("arguments[0].click();", element)
     
    cssPopUp = '.modal-body > div:nth-child(1) > div:nth-child(1) > h2:nth-child(1)'
    wait = WebDriverWait(driver, 10)
    wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, cssPopUp)))

    soupPerClick = BeautifulSoup(driver.page_source, 'html5lib')
    
    tabel = soupPerClick.select('.modal-body > div:nth-child(1) > div:nth-child(2)')
    
    if not headers:
        for i in tabel[0].findAll('th'):
            headers.append(i.text)
        del headers[1:3]
        del headers[6]
        del headers[8]
        headersFinal = [headers[0]]
        headersFinal.extend(['ODP ' + i for i in headers[4:6]])
        headersFinal.extend(['PDP ' + i for i in headers[-2:]])
        headersFinal.append(headers[1][:headers[1].find('f ')+1])
        headersFinal.extend(headers[2:4])
        headersFinal.insert(0, 'Kabupaten')
        headersFinal.insert(1, 'Kecamatan')
    
    Desa = []
    ODPPantau = []
    ODPSelesai = []
    PDPRawat = []
    PDPSelesai = []
    Positif = []
    Sembuh = []
    Meninggal = []

    Isi = tabel[0].findAll('td')

    seqDesa = np.arange(0, len(Isi), 10)
    seqODPPantau = np.arange(1, len(Isi), 10)
    seqODPSelesai = np.arange(2, len(Isi), 10)
    seqPDPRawat = np.arange(4, len(Isi), 10)
    seqPDPSelesai = np.arange(5, len(Isi), 10)
    seqPositif = np.arange(7, len(Isi), 10)
    seqSembuh = np.arange(8, len(Isi), 10)
    seqMeninggal = np.arange(9, len(Isi), 10)

    for idx, value in enumerate(Isi):
        if idx in seqDesa:
            Desa.append(value.text)
        elif idx in seqODPPantau:
            ODPPantau.append(int(value.text))
        elif idx in seqODPSelesai:
            ODPSelesai.append(int(value.text))
        elif idx in seqPDPRawat:
            PDPRawat.append(int(value.text))
        elif idx in seqPDPSelesai:
            PDPSelesai.append(int(value.text))
        elif idx in seqPositif:
            Positif.append(int(value.text))
        elif idx in seqSembuh:
            Sembuh.append(int(value.text))
        elif idx in seqMeninggal:
            Meninggal.append(int(value.text))
        
    dataPerKec = [Desa, 
              ODPPantau,
              ODPSelesai,
              PDPRawat,
              PDPSelesai,
              Positif,
              Sembuh,
              Meninggal]

    dataJembrana.append(dataPerKec)
    
    action.click()
    action.perform()
    
    driver.implicitly_wait(3)

driver.close()
# %%
Kecamatan = []
Desa = []
ODPPantau = []
ODPSelesai = []
PDPRawat = []
PDPSelesai = []
Positif = []
Sembuh = []
Meninggal = []
 
 # %%
def toCapital(string):
    return(string.capitalize())
 
for i, i_fill in enumerate(dataJembrana):
    Desa.extend(list(map(toCapital, dataJembrana[i][0])))
    lenDesa = len(dataJembrana[i][0])
    Kecamatan.extend([Kecamatan_temp[i] for j in range(lenDesa)])
    ODPPantau.extend(dataJembrana[i][1])
    ODPSelesai.extend(dataJembrana[i][2])
    PDPRawat.extend(dataJembrana[i][3])
    PDPSelesai.extend(dataJembrana[i][4])
    Positif.extend(dataJembrana[i][5])
    Sembuh.extend(dataJembrana[i][6])
    Meninggal.extend(dataJembrana[i][7])

# %%
Kabupaten = ['Jembrana' for i in range(len(Kecamatan))]
dataJembrana = [Kabupaten,
                Kecamatan,
                Desa,
                ODPPantau,
                ODPSelesai,
                PDPRawat,
                PDPSelesai,
                Positif,
                Sembuh,
                Meninggal]

# %%
df = pd.DataFrame(dataJembrana).transpose()
df.columns = headersFinal

# %%
TanggalRaw = soupJembrana.select_one('#kejadian > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > p:nth-child(3)').text
Tanggal = TanggalRaw[TanggalRaw.find(':')+2:]
Tanggal = datetime.datetime.strptime(Tanggal, "%d/%m/%Y").strftime("%Y-%m-%d")
Tanggal = [Tanggal for i in range(df.shape[0])]

now = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
TanggalWaktuScrape = [now for i in range(df.shape[0])]

df.insert(0, column='Tanggal Update', value=Tanggal)
df.insert(0, column='Tanggal Waktu Scrape', value=TanggalWaktuScrape)

SourceLink = [url for i in range(df.shape[0])]
df.insert(df.shape[1], column='Source Link', value=SourceLink)

# %%
print(df.head())

# %%
df.to_csv()
df.to_csv(r'B:\Projects\Work\Covid-19\Data Scraping Bali\Jembrana_' + Tanggal[0] + '.csv')
