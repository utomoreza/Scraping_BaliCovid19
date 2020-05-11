#!/usr/bin/env python
# coding: utf-8

# In[2]:


# import semua library yang diperlukan
import pandas as pd
import numpy as np
import datetime
import html5lib
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import datetime

# In[3]:


# masukkan alamat URL
url = 'http://covid19.banglikab.go.id/peta'


# In[4]:


# mulai otomasi browser menggunakan selenium
driver = webdriver.Firefox(executable_path='C:/Users/utomo/AppData/Local/Temp/webdriver/geckodriver.exe')
# driver = webdriver.Chrome(executable_path='C:/Users/utomo/AppData/Local/Temp/Rar$EXa0.185/chromedriver.exe')
driver.get(url)

# dan tunggu hingga browser secara sempurna menampilkan map di webpage
wait = WebDriverWait(driver, 10)
wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "section-top-border")))
print('ready to scrape.') # siap mulai scraping


# In[5]:


# lempar hasil selenium ke BeautifulSoup
soupBangli = BeautifulSoup(driver.page_source, 'html5lib')


# In[6]:


# matikan browser karena sudah tidak dibutuhkan lagi
driver.close()


# In[7]:


# ambil data Kecamatan beserta Kabupatennya
# data tsb berada di tag 'div' dengan atribut class 'col-md-3',
# lalu berada di tag 'h4'
KecKabRaw = []
for i in soupBangli.findAll('div', attrs={'class':'col-md-3'}):
    KecKabRaw.append(i.find('h4').text)
    
KecKabRaw


# In[8]:


### berhubung terdapat perubahan pada website,
### script di bawah ini sudah tidak bisa digunakan kembali
# pisahkan data Kecamatan Kabupaten tersebut
# Kecamatan = []
# Kabupaten = []
# for i in KecKabRaw:
#     Kecamatan.append(re.findall('an\s[A-Z]{1}[a-z]+', i)[0][3:])
    # Kabupaten.append(re.findall('en\s[A-Z]{1}[a-z]+', i)[0][3:])
    
### sebagai gantinya, gunakan script di bawah ini
# buat list berisi Kecamatan
Kecamatan = ['Bangli','Tembuku','Susut','Kintamani']
# buat list berisi Kabupaten
Kabupaten = ['Bangli' for i in range(len(Kecamatan))]

# print(Kecamatan)
# print(Kabupaten)


# In[9]:


# ambil isi tabel yang berada di tag 'div' dengan atribut class 'col-md-3',
# lalu berada di tag 'tr'
ContainRaw = []
for i in soupBangli.findAll('div', attrs={'class':'col-md-3'}):
    for j in i.findAll('tr'):
        ContainRaw.append(j.text)
    
# ContainRaw


# In[92]:


# isi tabel di variabel list ContainRaw di atas mengandung headers beserta data angkanya,
# sehingga dilakukan pemisahan
# pertama, kita pisahkan headersnya
headers = []
for i in range(5):
    headers.append(' '.join(re.findall('[a-zA-Z|&]+', ContainRaw[i])))

headers.insert(0, headers[0][:headers[0].find('an ')+2])
headers.insert(1, headers[1][headers[1].find('an ')+3:headers[1].find('i S')+1])
headers.insert(2, headers[2][headers[2].find('i S')+2:])
del headers[3]
headers.insert(3, headers[3][:headers[3].find('a M')+1])
headers.insert(4, headers[4][headers[4].find('a M')+2:headers[4].find('i S')+1])
headers.insert(5, headers[5][headers[5].find('i S')+2:])
del headers[6]
headers.insert(6, headers[6][:headers[6].find('n P')+1])
headers.insert(7, headers[7][headers[7].find('n P')+2:headers[7].find('s S')+1])
headers.insert(8, headers[8][headers[8].find('s S')+2:])
del headers[9]
headers.insert(9, headers[9][:headers[9].find('an D')+2])
headers.insert(10, headers[10][headers[10].find('an D')+3:headers[10].find('t P')+1])
headers.insert(11, headers[11][headers[11].find('t P')+2:])
del headers[12]
headers.insert(12, headers[12][:headers[12].find('f D')+1])
headers.insert(13, headers[13][headers[13].find('f D')+2:headers[13].find('t S')+1])
headers.insert(14, headers[14][headers[14].find('t S')+2:headers[14].find('h M')+1])
headers.insert(15, headers[15][headers[15].find('h M')+2:])
del headers[16]
# setelah itu, tambahkan header tambahan
headers.insert(0, 'Tanggal Update Web')
headers.insert(1, 'Waktu Update Web')
headers.insert(2, 'Kabupaten')
headers.insert(3, 'Kecamatan')
headers


# In[55]:


# buat variabel sequence sebagai looping untuk tiap isi kolom di dalam tabel hasil scraped
seqPP = np.arange(0, len(ContainRaw), 5)
seqOTG = np.arange(1, len(ContainRaw), 5)
seqODP = np.arange(2, len(ContainRaw), 5)
seqPDP = np.arange(3, len(ContainRaw), 5)
seqPositif = np.arange(4, len(ContainRaw), 5)


# In[56]:


# buat variabel list kosong sebagai penyimpan hasil tiap kolom
PPtotal = []
PPmasihIsolasi = []
PPselesaiIsolasi = []
OTGtotal = []
OTGmasihIsolasi = []
OTGselesaiIsolasi = []
ODPtotal = []
ODPproses = []
ODPselesai = []
PDPtotal = []
PDPdirawat = []
PDPpulangSehat = []
PositifTotal = []
PositifDirawat = []
PositifSembuh = []
PositifMeninggal = []


# In[90]:


# mulai lakukan looping untuk mengambil isi dari Pelaku Perjalanan, OTG, dst
# dan gunakan regex untuk membersihkannya dari characters yang mengganggu
for i in seqPP:
    PPtotal.append(int(''.join(re.findall('\d+\s\n', ContainRaw[i])[0])))
    PPmasihIsolasi.append(int(''.join(re.findall('\d+\s\n', ContainRaw[i])[1])))
    PPselesaiIsolasi.append(int(''.join(re.findall('\d+\s\n', ContainRaw[i])[2])))
    
for i in seqOTG:
    OTGtotal.append(int(''.join(re.findall('\d+\s\n', ContainRaw[i])[0])))
    OTGmasihIsolasi.append(int(''.join(re.findall('\d+\s\n', ContainRaw[i])[1])))
    OTGselesaiIsolasi.append(int(''.join(re.findall('\d+\s\n', ContainRaw[i])[2])))
    
for i in seqODP:
    ODPtotal.append(int(''.join(re.findall('\d+\s\n', ContainRaw[i])[0])))
    ODPproses.append(int(''.join(re.findall('\d+\s\n', ContainRaw[i])[1])))
    ODPselesai.append(int(''.join(re.findall('\d+\s\n', ContainRaw[i])[2])))
    
for i in seqODP:
    PDPtotal.append(int(''.join(re.findall('\d+\s\n', ContainRaw[i])[0])))
    PDPdirawat.append(int(''.join(re.findall('\d+\s\n', ContainRaw[i])[1])))
    PDPpulangSehat.append(int(''.join(re.findall('\d+\s\n', ContainRaw[i])[2])))
    
for i in seqPositif:
    PositifTotal.append(int(''.join(re.findall('\d+\s\n', ContainRaw[i])[0])))
    PositifDirawat.append(int(''.join(re.findall('\d+\s\n', ContainRaw[i])[1])))
    PositifSembuh.append(int(''.join(re.findall('\d+\s\n', ContainRaw[i])[2])))
    PositifMeninggal.append(int(''.join(re.findall('\d+\s\n', ContainRaw[i])[3])))


# In[84]:


# buat kolom Tanggal dan Waktu yang mana data tanggal waktunya didapatkan dari informasi di website
# informasi tanggalwaktu berada di tag 'div' dengan atribut class 'breadcrumb_iner_item',
# lalu di dalam tag 'h6' dan berada di urutan kedua
TanggalWaktu = soupBangli.find('div', attrs={'class':'breadcrumb_iner_item'}).findAll('h4')[1].text

# bersihkan data tanggalwaktu dari characters yang mengganggu
idxToGetDateTime = TanggalWaktu.find(',')+2
TanggalWaktu = TanggalWaktu[idxToGetDateTime:-1]

# pisahkan data tanggalwaktu menjadi tanggal dan waktu
idxToGetDate = TanggalWaktu.find(',')
Tanggal = TanggalWaktu[:idxToGetDate]
Waktu = TanggalWaktu[idxToGetDate+2:]


# In[87]:


# lalu buat menjadi list
Tanggal = [Tanggal for i in range(len(Kecamatan))]
Waktu = [Waktu for i in range(len(Kecamatan))]


# In[91]:


# gabung semua list menjadi list final
dataBangli = [Tanggal,
             Waktu,
             Kabupaten,
             Kecamatan,
             PPtotal,
             PPmasihIsolasi,
             PPselesaiIsolasi,
             OTGtotal,
             OTGmasihIsolasi,
             OTGselesaiIsolasi,
             ODPtotal,
             ODPproses,
             ODPselesai,
             PDPtotal,
             PDPdirawat,
             PDPpulangSehat,
             PositifTotal,
             PositifDirawat,
             PositifSembuh,
             PositifMeninggal]
# dataBangli


# In[95]:


# lalu ubah list final tsb menjadi sebuah dataframe lalu transpose
df = pd.DataFrame(dataBangli).transpose()
# set headers nya
df.columns = headers

now = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
TanggalWaktuScrape = [now for i in range(df.shape[0])]

df.insert(2, column='Tanggal Waktu Scrape', value=TanggalWaktuScrape)

SourceLink = [url for i in range(df.shape[0])]
df.insert(df.shape[1], column='Source Link', value=SourceLink)

print(df)


# In[ ]:


# export dataframe ke file csv
df.to_csv(r'B:\Projects\Work\Covid-19\Data Scraping Bali\Bangli_' + Tanggal[0] + '.csv')

