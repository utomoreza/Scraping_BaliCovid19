# import semua library yang diperlukan
import requests
import html5lib
from bs4 import BeautifulSoup
import numpy as np
import re
import pandas as pd
from random import randint
from time import sleep
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# masukkan alamat URL
url = "https://pendataan.baliprov.go.id/"

# buat object BeautifulSoup - mulai scraping
req = requests.get(url)
soup = BeautifulSoup(req.content, 'html5lib')

# cari posisi tabel di web
newTableRaw = soup.find('div', class_='table-responsive')

# ambil headers di web lalu modifikasi headers tsb
headers_temp = []
for i in newTableRaw.findAll('th'):   # headers berada di tag 'th'
    if re.match('\w+', i.text) != None:   # gunakan regex untuk membersihkan teks header
        headers_temp.append(i.text)

# perbaiki headers
headers_temp[-1] = headers_temp[-1] + '-' + headers_temp[5]
headers_temp[-2] = headers_temp[-2] + '-' + headers_temp[5]
del headers_temp[5]
del headers_temp[1]
headers = []
headers.append(headers_temp[0])
headers.extend(headers_temp[-2:])
headers.extend(headers_temp[4:-2])
headers.extend(headers_temp[1:4])
# headers

# buat variabel list kosong sebagai tempat menyimpan isi dari tabel
Kabupaten = []
Dirawat = []
Sembuh = []
Meninggal = []
PPDN = []
TransmisiLokal = []
PositifLainnya = []
TotalPositif = []
WNA_PPLN = []
WNI_PPLN = []

# ambil isi tabel. isinya berada di tag 'td'
fillNewTable = newTableRaw.findAll('td')

# buat variabel sequence sebagai looping untuk tiap jenis kolom di tabel
seqKabupaten = np.arange(0, len(fillNewTable), 10)
seqWNA_PPLN = np.arange(1, len(fillNewTable), 10)
seqWNI_PPLN = np.arange(2, len(fillNewTable), 10)
seqPPDN = np.arange(3, len(fillNewTable), 10)
seqTransmisiLokal = np.arange(4, len(fillNewTable), 10)
seqPositifLainnya = np.arange(5, len(fillNewTable), 10)
seqTotalPositif = np.arange(6, len(fillNewTable), 10)
seqDirawat = np.arange(7, len(fillNewTable), 10)
seqSembuh = np.arange(8, len(fillNewTable), 10)
seqMeninggal = np.arange(9, len(fillNewTable), 10)

# mulai looping isi tabel lalu ambil isinya dan pindahkan ke list-list yang telah dibuat di atas
for i in range(len(fillNewTable)):
    if i in seqKabupaten:
        Kabupaten.append(fillNewTable[i].text)
        
    elif i in seqWNA_PPLN:
        WNA_PPLN.append(int(fillNewTable[i].text))
    
    elif i in seqWNI_PPLN:
        WNI_PPLN.append(int(fillNewTable[i].text))
        
    elif i in seqPPDN:
        PPDN.append(int(fillNewTable[i].text))
        
    elif i in seqTransmisiLokal:
        TransmisiLokal.append(int(fillNewTable[i].text))
        
    elif i in seqPositifLainnya:
        PositifLainnya.append(int(fillNewTable[i].text))
        
    elif i in seqTotalPositif:
        TotalPositif.append(int(fillNewTable[i].text))
        
    elif i in seqDirawat:
        Dirawat.append(int(fillNewTable[i].text))
        
    elif i in seqSembuh:
        Sembuh.append(int(fillNewTable[i].text))
        
    elif i in seqMeninggal:
        Meninggal.append(int(fillNewTable[i].text))
        
# gabungkan semua list agar menjadi satu list utuh
dataBali = [Kabupaten,
           WNA_PPLN,
           WNI_PPLN,
           PPDN,
           TransmisiLokal,
           PositifLainnya,
           TotalPositif,
           Dirawat,
           Sembuh,
           Meninggal]

# ubah list utuh menjadi sebuah dataframe
dataBali_df = pd.DataFrame(dataBali).transpose()

# set headers
dataBali_df.columns = headers

# ambil data tanggal update dari website, lalu buat list dari tanggal tsb
tanggalRaw = soup.findAll('div', class_='card-header')[6].text
tanggal = re.findall('\d{2}\s\w+\s\d{4}', tanggalRaw)[0]
tanggal = [tanggal for i in range(dataBali_df.shape[0])]

# buat kolom baru 'Tanggal Update' dari data tanggal update
dataBali_df.insert(0, column='Tanggal Update', value=tanggal)

now = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
TanggalWaktuScrape = [now for i in range(dataBali_df.shape[0])]

dataBali_df.insert(1, column='Tanggal Waktu Scrape', value=TanggalWaktuScrape)

SourceLink = [url for i in range(dataBali_df.shape[0])]
dataBali_df.insert(dataBali_df.shape[1], column='Source Link', value=SourceLink)

print(dataBali_df)

# export dataframe ke file csv
dataBali_df.to_csv(r'B:\Projects\Work\Covid-19\Data Scraping Bali\Bali_' + tanggal[0] + '.csv')