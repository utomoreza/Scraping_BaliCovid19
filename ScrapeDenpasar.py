#!/usr/bin/env python
# coding: utf-8

# In[1]:


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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


# In[2]:


# masukkan alamat URL
url = 'https://safecity.denpasarkota.go.id/id/covid19'


# In[5]:


# mulai otomasi browser menggunakan selenium
driver = webdriver.Firefox(executable_path='C:/Users/utomo/AppData/Local/Temp/webdriver/geckodriver.exe')
driver.get(url)

# dan tunggu hingga browser secara sempurna menampilkan tabel yang diinginkan
wait = WebDriverWait(driver, 10)
wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "table-responsive")))
print('ready to scrape.') # siap mulai scraping


# In[6]:


# lempar hasil selenium ke BeautifulSoup
soupDenpasar = BeautifulSoup(driver.page_source, 'html5lib')


# In[7]:


# matikan browser karena sudah tidak dibutuhkan lagi
driver.close()


# In[8]:


# ambil data raw header yang berada di tag 'table',
# dengan atribut class 'table table-striped table-bordered',
# lalu berada di tag 'th'
headersTemp = [] # buat list sebagai penampung sementara
for i in soupDenpasar.findAll('table', attrs={'class':'table table-striped table-bordered'})[1].findAll('th'):
    headersTemp.append(i.text)
# headersTemp


# In[19]:


# bersihkan header raw dari character yang mengganggu
headers = [] # buat list sebagai penampung sementara
for i in headersTemp:
    headers.append(''.join(re.findall('\w', i)))

# lalu dari headers di atas, modifikasi headers tersebut dengan tambahan beberapa kolom baru,
# agar menyesuaikan dengan data yang ada di webpage
headersFinal = headers.copy()    
headersFinal.insert(2, 'OTG-Total')
headersFinal.insert(3, 'OTG-TelahIsolasiMandiri14HariTanpaGejala')
headersFinal.insert(4, 'OTG-Masih')
del headersFinal[5]
headersFinal.insert(5, 'ODP-Total')
headersFinal.insert(6, 'ODP-TelahIsolasiMandiri14HariTanpaGejala')
headersFinal.insert(7, 'ODP-Masih')
del headersFinal[8]
headersFinal.insert(8, 'PDP-Total')
headersFinal.insert(9, 'PDP-HasilLabNegatif')
headersFinal.insert(10, 'PDP-MenungguHasilLab')
del headersFinal[11]
headersFinal.insert(11, 'Positif-Total')
headersFinal.insert(12, 'Positif-Sembuh')
headersFinal.insert(13, 'Positif-Meninggal')
headersFinal.insert(14, 'Positif-MasihDirawat')
del headersFinal[15]
del headersFinal[0]
headersFinal.insert(0, 'KabupatenKota')

# print(headers)
# print(headersFinal)


# In[10]:


# ambil isi dari tabel
# isinya berada di tag 'table' dengan atribut class 'table table-striped table-bordered',
# lalu berada di tag 'td'
containTemp = [] # buat list sebagai penampung sementara
for i,j in enumerate(soupDenpasar.findAll('table', attrs={'class':'table table-striped table-bordered'})[1].findAll('td')):
    containTemp.append(j.text)
# containTemp[2]


# In[11]:


# lalu bersihkan isi tabel dari characters yang mengganggu
contain = [] # buat list sebagai penampung isi tabel
for i in containTemp:
    contain.append(''.join(re.findall('[a-zA-Z0-9]+', i)))
# contain[0:6]


# In[12]:


# buat variabel sequence sebagai looping untuk tiap isi kolom di dalam tabel hasil scraped
seqDesaKel = np.arange(1, len(contain), 6)
seqOTG = np.arange(2, len(contain), 6)
seqODP = np.arange(3, len(contain), 6)
seqPDP = np.arange(4, len(contain), 6)
seqPositif = np.arange(5, len(contain), 6)


# In[13]:


# buat variabel list kosong sebagai penyimpan hasil tiap kolom
DesaKel = []
OTG = []
ODP = []
PDP = []
Positif = []

# mulai lakukan looping untuk mengambil isi dari DesaKel, OTG, dst
for i in seqDesaKel:
    DesaKel.append(contain[i])    
for i in seqOTG:
    OTG.append(contain[i])
for i in seqODP:
    ODP.append(contain[i])    
for i in seqPDP:
    PDP.append(contain[i])    
for i in seqPositif:
    Positif.append(contain[i])
    
# print(DesaKel[:6])
# print(OTG[:6])
# print(ODP[:6])
# print(PDP[:6])
# print(Positif[:6])


# In[14]:


# buat list kosong untuk menyimpan data tambahan dari variabel OTG di atas,
# yaitu OTG Total, OTG Telah Isolasi Mandiri 14 Hari Tanpa Gejala, dan OTG yang masih berstatus OTG
OTG_Total = []
OTG_TelahIsolasiMandiri14HariTanpaGejala = []
OTG_Masih = []

# mulai lakukan looping ke dalam variabel OTG,
# lalu pisah isinya menjadi 3 bagian menggunakan regex
for i in OTG:
    if re.match('^[0-9]+$', i) != None:
        OTG_Total.append(i)
        OTG_TelahIsolasiMandiri14HariTanpaGejala.append(np.NaN)
        OTG_Masih.append(np.NaN)
    else:
        OTG_Total.append(re.findall('^[0-9]+', i)[0][0:])
        OTG_TelahIsolasiMandiri14HariTanpaGejala.append(re.findall('[a][0-9]+', i)[0][1:])
        OTG_Masih.append(re.findall('[G][0-9]+', i)[0][1:])
        
# print(OTG_Total[:6])
# print(OTG_TelahIsolasiMandiri14HariTanpaGejala[:6])
# print(OTG_Masih[:6])


# In[15]:


# buat list kosong untuk menyimpan data tambahan dari variabel ODP di atas,
# yaitu ODP Total, ODP Telah Isolasi Mandiri 14 Hari Tanpa Gejala, dan ODP yang masih berstatus ODP
ODP_Total = []
ODP_TelahIsolasiMandiri14HariTanpaGejala = []
ODP_Masih = []

# mulai lakukan looping ke dalam variabel ODP,
# lalu pisah isinya menjadi 3 bagian menggunakan regex
for i in ODP:
    if re.match('^[0-9]+$', i) != None:
        ODP_Total.append(i)
        ODP_TelahIsolasiMandiri14HariTanpaGejala.append(np.NaN)
        ODP_Masih.append(np.NaN)
    else:
        ODP_Total.append(re.findall('^[0-9]+', i)[0][0:])
        ODP_TelahIsolasiMandiri14HariTanpaGejala.append(re.findall('[a][0-9]+', i)[0][1:])
        ODP_Masih.append(re.findall('[P][0-9]+', i)[0][1:])
        
# print(ODP_Total[:6])
# print(ODP_TelahIsolasiMandiri14HariTanpaGejala[:6])
# print(ODP_Masih[:6])


# In[16]:


# buat list kosong untuk menyimpan data tambahan dari variabel PDP di atas,
# yaitu PDP Total, PDP dengan hasil lab negatif, dan PDP yang masih menunggu hasil lab
PDP_Total = []
PDP_HasilLabNegatif = []
PDP_MenungguHasilLab = []

# mulai lakukan looping ke dalam variabel PDP,
# lalu pisah isinya menjadi 3 bagian menggunakan regex
for i in PDP:
    if re.match('^[0-9]+$', i) != None:
        PDP_Total.append(i)
        PDP_HasilLabNegatif.append(np.NaN)
        PDP_MenungguHasilLab.append(np.NaN)
    else:
        PDP_Total.append(re.findall('^[0-9]+', i)[0][:])
        PDP_HasilLabNegatif.append(re.findall('[f][0-9]+', i)[0][1:])
        PDP_MenungguHasilLab.append(re.findall('[b][0-9]+', i)[0][1:])
        
# print(PDP_Total[:6])
# print(PDP_HasilLabNegatif[:6])
# print(PDP_MenungguHasilLab[:6])


# In[17]:


# buat list kosong untuk menyimpan data tambahan dari variabel Positif di atas,
# yaitu Positif Total, Positif yang sembuh, Positif yang meninggal, dan Positif masih dirawat
Positif_Total = []
Positif_Sembuh = []
Positif_Meninggal = []
Positif_MasihDirawat = []

# mulai lakukan looping ke dalam variabel Positif,
# lalu pisah isinya menjadi 4 bagian menggunakan regex
for i in Positif:
    if re.search('^[0-9]+$', i) != None:
        Positif_Total.append(i)
        Positif_Sembuh.append(np.NaN)
        Positif_Meninggal.append(np.NaN)
        Positif_MasihDirawat.append(np.NaN)
        
    else:
        Positif_Total.append(re.findall('^[0-9]+', i)[0][:])
        
        if re.search('Sembuh', i) != None:
            Positif_Sembuh.append(re.findall('[h][0-9]+', i)[0][1:])
        else:
            Positif_Sembuh.append(np.NaN)
    
        if re.search('Meninggal', i) != None:
            Positif_Meninggal.append(re.findall('[l][0-9]+', i)[0][1:])
        else:
            Positif_Meninggal.append(np.NaN)
    
        if re.search('MasihDirawat', i) != None:
            Positif_MasihDirawat.append(re.findall('[t][0-9]+', i)[0][1:])
        else:
            Positif_MasihDirawat.append(np.NaN)
      
# print(Positif_Total[:6])
# print(Positif_Sembuh[:6])
# print(Positif_Meninggal[:6])
# print(Positif_MasihDirawat[:6])


# In[20]:


# buat list KabKota yang berisi 'Denpasar'
KabKota = ['Denpasar' for i in range(len(DesaKel))]

# gabung semua list menjadi satu variabel list final
dataDenpasar = [KabKota,
                DesaKel,
                OTG_Total,
                OTG_TelahIsolasiMandiri14HariTanpaGejala,
                OTG_Masih,
                ODP_Total,
                ODP_TelahIsolasiMandiri14HariTanpaGejala,
                ODP_Masih,
                PDP_Total,
                PDP_HasilLabNegatif,
                PDP_MenungguHasilLab,
                Positif_Total,
                Positif_Sembuh,
                Positif_Meninggal,
                Positif_MasihDirawat]


# In[21]:


# ubah list final menjadi sebuah dataframe, lalu transpose
df = pd.DataFrame(dataDenpasar).transpose()
# df.head()


# In[22]:


# set header-nya
df.columns = headersFinal
# df.head()


# In[23]:


# buat kolom tanggal yang berisi informasi tanggal hari ini
# berhubung di webpage tidak terdapat informasi tanggal data terakhir diupdate,
# jadinya kita perlu menentukan sendiri data tanggalnya
# Tanggal = [datetime.date.today() for i in DesaKel]

now = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
TanggalWaktuScrape = [now for i in DesaKel]

# masukkan data Tanggal tersebut ke index ke-0 dengan nama kolom 'Tanggal-Scraped',
# berhubung data tanggal tsb adalah data kita melakukan scraping, 
# bukan data update langsung dari website nya
# df.insert(0, column='Tanggal-Scraped', value=Tanggal)
df.insert(0, column='Tanggal Waktu Scrape', value=TanggalWaktuScrape)
# df.head()


# In[24]:


# definisikan sebuah dictionary yang berisi zona tiap desa
Zones = {'Kuning': ['Serangan', 'Pedungan', 'Sesetan', 'PemecutanKelod', 'TegalHarum', 'Padangsambian',
                    'DanginPuriKaja', 'KesimanPetilan'],
         'Hijau': ['DanginPuriKelod', 'DanginPuriKauh'],
         'Biru': ['PadangsambianKelod'],
         'Ungu': ['Renon', 'SumertaKelod', 'DauhPuri', 'DauhPuriKangin', 'Pemecutan', 'DanginPuri',
                  'DanginPuriKangin', 'Sumerta', 'SumertaKaja', 'DauhPuriKaja', 'PenatihDanginPuri',
                  'PeguyanganKaja'],
         'Merah': ['Pemogan', 'Sidakarya', 'SanurKauh', 'Sanur', 'Panjer', 'SanurKaja', 'Kesiman', 
                   'KesimanKertalangu', 'DauhPuriKauh', 'TegalKertha', 'SumertaKauh', 'Tonja', 
                   'Penatih', 'Peguyangan', 'UbungKaja'],
         'MerahMuda': ['DauhPuriKelod', 'PemecutanKaja', 'PadangsambianKaja', 'Ubung', 'PeguyanganKangin']}


# In[25]:


# buat function yang akan memetakan zona dengan desanya di dataframe
def fitZone(x):
    global Zones
    for i in Zones.keys():
        if x in Zones[i]:
            return(i)


# In[26]:


# buat list yang berisi hasil pemetaan antara zona dengan urutan nama desa di dataframe
Zona = list(map(fitZone, list(df['DesaKelurahan'])))


# In[27]:


# masukan data Zona ke index ke-3 dan namai kolomnya 'Zona'
df.insert(3, column='Zona', value=Zona)
# df.head()


# In[28]:


# definisikan sebuah dictionary yang berisi nama kecamatan tiap desa
KecKel = {'DenpasarBarat': ['DauhPuriKangin', 'DauhPuriKauh', 'DauhPuriKelod', 'PadangsambianKaja', 'PadangsambianKelod',
                               'PemecutanKelod', 'TegalHarum', 'TegalKertha', 'DauhPuri', 'Padangsambian', 'Pemecutan'],
             'DenpasarSelatan': ['Pemogan', 'SanurKaja', 'SanurKauh', 'Sidakarya', 'Panjer', 'Pedungan', 'Renon', 
                                 'Sanur', 'Serangan', 'Sesetan'],
             'DenpasarTimur': ['DanginPuriKelod', 'KesimanKertalangu', 'KesimanPetilan', 'PenatihDanginPuri', 
                               'SumertaKaja', 'SumertaKauh', 'SumertaKelod', 'DanginPuri', 'Kesiman', 'Penatih', 'Sumerta'],
             'DenpasarUtara': ['DanginPuriKaja', 'DanginPuriKangin', 'DanginPuriKauh', 'DauhPuriKaja', 'PeguyanganKaja',
                               'PeguyanganKangin', 'PemecutanKaja', 'UbungKaja', 'Peguyangan', 'Tonja', 'Ubung']}


# In[29]:


# buat function yang akan memetakan kecamatan dengan desanya di dataframe
def fitKecKel(x):
    global KecKel
    for i in KecKel.keys():
        if x in KecKel[i]:
            return(i)


# In[30]:


# buat list yang berisi hasil pemetaan antara kecamatan dengan urutan nama desa di dataframe
Kecamatan = list(map(fitKecKel, df['DesaKelurahan']))


# In[31]:


# masukan data Zona ke index ke-2 dan namai kolomnya 'Kecamatan'
df.insert(2, column='Kecamatan', value=Kecamatan)
# df.head()


# In[ ]:

SourceLink = [url for i in range(df.shape[0])]
df.insert(df.shape[1], column='Source Link', value=SourceLink)

print(df)


# In[ ]:


# export dataframe ke file csv
Tanggal = datetime.date.today()

df.to_csv(r'B:\Projects\Work\Covid-19\Data Scraping Bali\Denpasar_' + str(Tanggal) + '.csv')

