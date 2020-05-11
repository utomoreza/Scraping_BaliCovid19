#!/usr/bin/env python
# coding: utf-8

# # Gianyar https://covid19.gianyarkab.go.id/peta#pills-profile

# In[1]:


# import semua library yang diperlukan
import requests
import html5lib
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import re
import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import datetime

# In[2]:


# setDateToScrape = '23042020' # format ddmmyyyy


# In[2]:


url = 'https://covid19.gianyarkab.go.id/peta'

req = requests.get(url)
soup_Gianyar = BeautifulSoup(req.content, 'html5lib')


# ## Tabel Kumulatif

# In[4]:


# totalKab = soup_Gianyar.findAll('tbody', attrs={'class':None})[1]
# totalKab_ = totalKab.findAll('div', attrs={'class':'badge badge-pill badge-outline-danger'})

# Lainnya = []
# ODP = []
# PDP = []
# OTG = []
# Positif = []

# for i in np.arange(0,4):
#     contain = int(''.join(re.findall('\d', totalKab_[i].text)))
#     Lainnya.append(contain)

# for i in np.arange(4,8):
#     contain = int(''.join(re.findall('\d', totalKab_[i].text)))
#     ODP.append(contain)

# for i in np.arange(8,12):
#     contain = int(''.join(re.findall('\d', totalKab_[i].text)))
#     PDP.append(contain)
    
# for i in np.arange(12,16):
#     contain = int(''.join(re.findall('\d', totalKab_[i].text)))
#     OTG.append(contain)
    
# for i in np.arange(16,20):
#     contain = int(''.join(re.findall('\d', totalKab_[i].text)))
#     Positif.append(contain)
    
# tabel_totalKab = [Lainnya, ODP, PDP, OTG, Positif]
# tabel_totalKab


# In[5]:


# headerTotal = ['Penanganan', 'Lepas Penanganan', 'Meninggal', 'Jumlah']


# In[6]:


# totalKab_Gianyar = pd.DataFrame(tabel_totalKab, columns=headerTotal)


# In[11]:


# driver = webdriver.Chrome(executable_path='C:/Users/utomo/AppData/Local/Temp/Rar$EXa0.185/chromedriver.exe')
# driver.get(url)

# wait = WebDriverWait(driver, 10)
# wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "card")))
# print('ready to scrape.')


# In[12]:


# xpath = '//a[@class="nav-link"][@id="pills-profile-tab"][text()="Tabel Persebaran Kasus"]'
# cursor = driver.find_element_by_xpath(xpath)
# cursor.click()


# In[13]:


# tabelSebaranKasus = BeautifulSoup(driver.page_source, 'html5lib')


# In[14]:


# StatusRaw = tabelSebaranKasus.findAll('table', class_='table table-striped table-bordered')[0].text
# Status = []
# Status.append(StatusRaw[:7])
# Status.append(StatusRaw[7:10])
# Status.append(StatusRaw[10:13])
# Status.append(StatusRaw[13:16])
# Status.append(StatusRaw[16:23])
# Status


# In[15]:


# totalKab_Gianyar.insert(0, column='Status', value=Status)
# totalKab_Gianyar


# In[16]:


# # dateToSave = datetime.datetime.strptime(setDateToScrape, '%d%m%Y').strftime('%Y-%m-%d')
# totalKab_Gianyar['Tanggal Scraped'] = [datetime.date.today() for i in range(len(Status))]

# totalKab_Gianyar.to_csv('totalKab_Gianyar_' + str(datetime.date.today()) + '.csv')


# In[17]:


# driver.close()


# ## Tabel Luar Wilayah

# In[18]:


# luarWilayah = soup_Gianyar.findAll('tbody', attrs={'class':None})[3]
# luarWilayah_ = luarWilayah.findAll('div', attrs={'class':'badge badge-pill badge-outline-danger'})

# Lainnya = []
# ODP = []
# PDP = []
# OTG = []
# Positif = []

# for i in np.arange(0,4):
#     contain = int(''.join(re.findall('\d', luarWilayah_[i].text)))
#     Lainnya.append(contain)

# for i in np.arange(4,8):
#     contain = int(''.join(re.findall('\d', luarWilayah_[i].text)))
#     ODP.append(contain)

# for i in np.arange(8,12):
#     contain = int(''.join(re.findall('\d', luarWilayah_[i].text)))
#     PDP.append(contain)
    
# for i in np.arange(12,16):
#     contain = int(''.join(re.findall('\d', luarWilayah_[i].text)))
#     OTG.append(contain)
    
# for i in np.arange(16,20):
#     contain = int(''.join(re.findall('\d', luarWilayah_[i].text)))
#     Positif.append(contain)
    
# tabel_luarWilayah = [Lainnya, ODP, PDP, OTG, Positif]
# tabel_luarWilayah


# In[19]:


# luarWilayah_Gianyar = pd.DataFrame(tabel_luarWilayah, columns=headerTotal)
# luarWilayah_Gianyar.insert(0, column='Status', value=Status)
# luarWilayah_Gianyar


# In[20]:


# luarWilayah_Gianyar['Tanggal Scraped'] = [datetime.date.today() for i in range(len(Status))]

# luarWilayah_Gianyar.to_csv('luarWilayah_Gianyar_' + str(datetime.date.today()) + '.csv')


# ## Tabel Desa/Kelurahan

# In[2]:


# masukkan alamat URL
url = 'https://covid19.gianyarkab.go.id/peta'

# mulai scraping dengan menggunakan library requests
# dan simpan hasil scraping di variabel soup_Gianyar
req = requests.get(url)
soup_Gianyar = BeautifulSoup(req.content, 'html5lib')


# In[3]:


# mulai otomasi browser menggunakan selenium
driver = webdriver.Firefox(executable_path='C:/Users/utomo/AppData/Local/Temp/webdriver/geckodriver.exe')
driver.get(url)

# dan tunggu hingga browser secara sempurna menampilkan map di webpage
wait = WebDriverWait(driver, 10)
wait.until(EC.visibility_of_all_elements_located((By.ID, "map2")))
print('ready to scrape.') # siap mulai scraping


# In[4]:


# scroll ke bawah sebanyak 750 pixel.
# hal ini dibutuhkan untuk mengantisipasi error saat selenium akan mengklik tab yang diinginkan,
# dan berhubung tabnya berada di tengah webpage, kita perlu memerintahkan selenium untuk scroll down
driver.execute_script("window.scrollTo(0, 850)") 

# tunggu 2 detik agar webpage merespon
driver.implicitly_wait(2)


# In[5]:


# definisikan xpath yang akan digunakan sebagai posisi untuk diklik oleh selenium
xpath = '//a[@class="nav-link"][@id="pills-profile-tab"][text()="Tabel Persebaran Kasus"]'

# perintahkan selenium untuk mengklik tab dengan menggunakan xpath yang telah diberikan
cursor = driver.find_element_by_xpath(xpath)
cursor.click()


# In[6]:


# tunggu 2 detik agar webpage merespon
driver.implicitly_wait(2)

# lempar hasil klik ke BeautifulSoup
tabelSebaranKasus = BeautifulSoup(driver.page_source, 'html5lib')


# In[7]:


# matikan browser karena sudah tidak dibutuhkan lagi
driver.close()


# In[13]:


# ambil header dari tabel yang diinginkan
# header berada di tag 'thead' tanpa atribut class dan berada di urutan keempat
# lalu berada di tag 'th'
header_BasedOnDesa = soup_Gianyar.findAll('thead', attrs={'class':None})[4]
header_BasedOnDesa_ = header_BasedOnDesa.findAll('th')

# setelah headers raw didapatkan, bersihkan headers tersebut dari character yang tak dibutuhkan
headers = []
for i,j in enumerate(header_BasedOnDesa_):
    if i >= 3:
        headers.append(''.join(re.findall('\w', header_BasedOnDesa_[i].text)))
    else:
        headers.append(header_BasedOnDesa_[i].text)
headers = headers[1:] # kita tidak membutuhkan nama kolom pertama, yaitu 'No.'. jadi kita cukup membuangnya


# In[17]:


# berhubung isi variable headers di atas tidak berada di urutan yang tepat,
# kita perlu memperbaiki urutannya, dan menyimpan hasilnya di variabel headersFinal
headersFinal = []
headersFinal.append('Kabupaten')
headersFinal.append(headers[1])
headersFinal.append(headers[0])
headersFinal.extend(headers[2:])
# headersFinal


# In[24]:


# buat variabel sequence sebagai looping untuk tiap isi kolom di dalam tabel hasil scraped
seqDesa = np.arange(1, len(tabelSebaranKasus.find('tbody', attrs={'class':'item-desa'}).findAll('td')), 9)
seqKec = np.arange(2, len(tabelSebaranKasus.find('tbody', attrs={'class':'item-desa'}).findAll('td')), 9)
seqLepas = np.arange(3, len(tabelSebaranKasus.find('tbody', attrs={'class':'item-desa'}).findAll('td')), 9)
seqLain = np.arange(4, len(tabelSebaranKasus.find('tbody', attrs={'class':'item-desa'}).findAll('td')), 9)
seqODP = np.arange(5, len(tabelSebaranKasus.find('tbody', attrs={'class':'item-desa'}).findAll('td')), 9)
seqPDP = np.arange(6, len(tabelSebaranKasus.find('tbody', attrs={'class':'item-desa'}).findAll('td')), 9)
seqOTG = np.arange(7, len(tabelSebaranKasus.find('tbody', attrs={'class':'item-desa'}).findAll('td')), 9)
seqPositif = np.arange(8, len(tabelSebaranKasus.find('tbody', attrs={'class':'item-desa'}).findAll('td')), 9)


# In[43]:


# ambil konten dari tabel yang diinginkan
# tabel tsb berada di tag 'tbody' dengan atribut class 'item-desa',
# lalu di tag 'td'
tabelDesa = tabelSebaranKasus.find('tbody', attrs={'class':'item-desa'}).findAll('td')

# buat variabel list kosong sebagai penyimpan hasil tiap kolom
Desa = []
Kec = []
Lepas = []
Lain = []
ODP = []
PDP = []
OTG = []
Positif = []

# mulai lakukan looping untuk mengambil isi dari Desa, Kec, Lepas, dst
for i in seqDesa:
    Desa.append(tabelDesa[i].text)
for i in seqKec:
    Kec.append(tabelDesa[i].text)
for i in seqLepas:
    Lepas.append(tabelDesa[i].text)
for i in seqLain:
    Lain.append(tabelDesa[i].text)
for i in seqODP:
    ODP.append(tabelDesa[i].text)    
for i in seqPDP:
    PDP.append(tabelDesa[i].text)    
for i in seqOTG:
    OTG.append(tabelDesa[i].text)    
for i in seqPositif:
    Positif.append(tabelDesa[i].text)

# Buat list yang berisi 'Gianyar'
Kab = ['Gianyar' for i in range(len(Kec))]
    
# combine semua list
DataBerdasarDesa = [Kab, Kec, Desa, Lepas, Lain, ODP, PDP, OTG, Positif]
# DataBerdasarDesa


# In[44]:


# buat list gabungan tersebut menjadi sebuah dataframe, lalu transpose
dataGianyar = pd.DataFrame(DataBerdasarDesa).transpose()

# set header-nya
dataGianyar.columns = headersFinal
# dataGianyar.head()


# In[45]:


# buat kolom Tanggal yang mana data tanggalnya didapatkan dari informasi di website
# informasi tanggal berada di tag 'p' dengan atribut class 'text-left'
tanggalRaw = tabelSebaranKasus.find('p', class_='text-left').text

# setelah data raw tanggal didapatkan, bersihkan data tersebut dari character yang mengganggu
tanggal = tanggalRaw[tanggalRaw.find(':')+2:]
# lalu buat menjadi sebuah list
tanggal = [tanggal for i in range(dataGianyar.shape[0])]

# code di bawah ini digunakan jika anda ingin membuat list Tanggal dari informasi tanggal hari ini
# dataGianyar['Tanggal Scraped'] = [datetime.date.today() for i in range(dataGianyar.shape[0])]


# In[46]:


# masukkan data tanggal ke kolom di index ke-0, dan namai kolomnya dengan'Tanggal Update'
dataGianyar.insert(0, column='Tanggal Update', value=tanggal)


# In[47]:

now = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
TanggalWaktuScrape = [now for i in range(dataGianyar.shape[0])]

dataGianyar.insert(1, column='Tanggal Waktu Scrape', value=TanggalWaktuScrape)

SourceLink = [url for i in range(dataGianyar.shape[0])]
dataGianyar.insert(dataGianyar.shape[1], column='Source Link', value=SourceLink)

print(dataGianyar)


# In[29]:


# export dataframe ke file csv
dataGianyar.to_csv(r'B:\Projects\Work\Covid-19\Data Scraping Bali\Gianyar_' + tanggal[0] + '.csv')


# In[ ]:




