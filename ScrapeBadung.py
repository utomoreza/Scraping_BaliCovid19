#!/usr/bin/env python
# coding: utf-8

# # https://covid19.badungkab.go.id/

# In[1]:


# import semua library yang diperlukan
import requests
import html5lib
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


# In[2]:


# masukkan alamat URL
url = 'https://covid19.badungkab.go.id/pemantauan-covid'

# buat object BeautifulSoup - mulai scraping
req_badung = requests.get(url)
soupBadung = BeautifulSoup(req_badung.content, 'html5lib')


# In[3]:


# simpan data dari tabel di tag 'table' dengan atribut class 'table table-bordered'
tables = soupBadung.findAll('table', attrs={'class':'table table-bordered'})

# buat list kosong untuk menyimpan isi tiap kolom
listDesa = []
listODPjumlah = []
listODPmasihPantau = []
listODPkeluarSelesai = []
listPDPjumlahKasus = []
listNegatif = []
listPositif = []
listBelumKeluar = []
listMasihRawat = []
listSembuh = []

# lakukan looping sepanjang data tables
for i in np.arange(1, len(tables)):
    # ambil data ke-i dari tables
    table = tables[i]
    
    # ambil data nama desa yang berada di tag 'td' tanpa atribut class
    findDesa = table.findAll('td', attrs={'class':None})
    Desa = [] # buat list kosong yang akan menyimpan nama desa tiap kecamatan
    # lakukan looping tiap kecamatan yang akan mengambil semua nama desa per kecamatan
    # data desa berada mulai dari index ke-0 seterusnya dengan kelipatan 10,
    # hingga panjang variabel findDesa dikurang 18
    for i in np.arange(0,len(findDesa)-18,10):
        Desa.append(findDesa[i].text)
        
    # ambil data ODPJumlah yang berada di tag 'th' tanpa atribut class
    findODPjumlah = table.findAll('th', attrs={'class':None})
    ODPjumlah = [] # buat list kosong yang akan menyimpan ODPJumlah tiap kecamatan
    # lakukan looping tiap kecamatan yang akan mengambil semua ODPJumlah per kecamatan
    # data ODPJumlah berada mulai dari index ke-2 seterusnya dengan kelipatan 19,
    # hingga panjang variabel findODPjumlah dikurang 18 
    for i in np.arange(2,len(findODPjumlah)-18,19):
        ODPjumlah.append(findODPjumlah[i].text)
    ODPJumlah = [int(i) for i in ODPjumlah] # ubah menjadi integer
    
    # ambil data ODPmasihPantau yang berada di tag 'th' tanpa atribut class
    findODPmasihPantau = table.findAll('th', attrs={'class':None})
    ODPmasihPantau = [] # buat list kosong yang akan menyimpan ODPmasihPantau tiap kecamatan
    # lakukan looping tiap kecamatan yang akan mengambil semua ODPmasihPantau per kecamatan
    # data ODPmasihPantau berada mulai dari index ke-5 seterusnya dengan kelipatan 19,
    # hingga panjang variabel findODPmasihPantau dikurang 18
    for i in np.arange(5,len(findODPmasihPantau)-18,19):
        ODPmasihPantau.append(findODPmasihPantau[i].text)
    ODPmasihPantau = [int(i) for i in ODPmasihPantau] # ubah menjadi integer
    
    # ambil data ODPkeluarSelesai yang berada di tag 'th' tanpa atribut class
    findODPkeluarSelesai = table.findAll('th', attrs={'class':None})
    ODPkeluarSelesai = [] # buat list kosong yang akan menyimpan ODPkeluarSelesai tiap kecamatan
    # lakukan looping tiap kecamatan yang akan mengambil semua ODPkeluarSelesai per kecamatan
    # data ODPkeluarSelesai berada mulai dari index ke-8 seterusnya dengan kelipatan 19,
    # hingga panjang variabel findODPkeluarSelesai dikurang 18
    for i in np.arange(8,len(findODPkeluarSelesai)-18,19):
        ODPkeluarSelesai.append(findODPkeluarSelesai[i].text)
    ODPkeluarSelesai = [int(i) for i in ODPkeluarSelesai] # ubah menjadi integer
    
    # ambil data PDPjumlahKasus yang berada di tag 'th' tanpa atribut class
    findPDPjumlahKasus = table.findAll('th', attrs={'class':None})
    PDPjumlahKasus = [] # buat list kosong yang akan menyimpan PDPjumlahKasus tiap kecamatan
    # lakukan looping tiap kecamatan yang akan mengambil semua PDPjumlahKasus per kecamatan
    # data PDPjumlahKasus berada mulai dari index ke-11 seterusnya dengan kelipatan 19,
    # hingga panjang variabel findPDPjumlahKasus dikurang 18
    for i in np.arange(11,len(findPDPjumlahKasus)-18,19):
        PDPjumlahKasus.append(findPDPjumlahKasus[i].text)
    PDPjumlahKasus = [int(i) for i in PDPjumlahKasus] # ubah menjadi integer
    
    # ambil data Negatif yang berada di tag 'td' tanpa atribut class
    findNegatif = table.findAll('td', attrs={'class': None})
    Negatif = [] # buat list kosong yang akan menyimpan Negatif tiap kecamatan
    # lakukan looping tiap kecamatan yang akan mengambil semua Negatif per kecamatan
    # data Negatif berada mulai dari index ke-3 seterusnya dengan kelipatan 10,
    # hingga panjang variabel findNegatif dikurang 15
    for i in np.arange(3,len(findNegatif)-15,10):
        Negatif.append(findNegatif[i].text)
    Negatif = [int(i) for i in Negatif] # ubah menjadi integer
    
    # ambil data Positif yang berada di tag 'td' tanpa atribut class
    findPositif = table.findAll('td', attrs={'class': None})
    Positif = [] # buat list kosong yang akan menyimpan Positif tiap kecamatan
    # lakukan looping tiap kecamatan yang akan mengambil semua Positif per kecamatan
    # data Positif berada mulai dari index ke-6 seterusnya dengan kelipatan 10,
    # hingga panjang variabel findPositif dikurang 12
    for i in np.arange(6,len(findPositif)-12,10):
        Positif.append(findPositif[i].text)
    Positif = [int(i) for i in Positif] # ubah menjadi integer
    
    # ambil data BelumKeluar yang berada di tag 'td' tanpa atribut class
    findBelumKeluar = table.findAll('td', attrs={'class': None})
    BelumKeluar = [] # buat list kosong yang akan menyimpan BelumKeluar tiap kecamatan
    # lakukan looping tiap kecamatan yang akan mengambil semua BelumKeluar per kecamatan
    # data BelumKeluar berada mulai dari index ke-9 seterusnya dengan kelipatan 10,
    # hingga panjang variabel findBelumKeluar dikurang 9
    for i in np.arange(9,len(findBelumKeluar)-9,10):
        BelumKeluar.append(findBelumKeluar[i].text)
    BelumKeluar = [int(i) for i in BelumKeluar] # ubah menjadi integer
    
    # ambil data MasihRawat yang berada di tag 'th' tanpa atribut class
    findMasihRawat = table.findAll('th', attrs={'class':None})
    MasihRawat = [] # buat list kosong yang akan menyimpan MasihRawat tiap kecamatan
    # lakukan looping tiap kecamatan yang akan mengambil semua MasihRawat per kecamatan
    # data MasihRawat berada mulai dari index ke-15 seterusnya dengan kelipatan 19,
    # hingga panjang variabel findMasihRawat dikurang 18
    for i in np.arange(15,len(findMasihRawat)-18,19):
        MasihRawat.append(findMasihRawat[i].text)
    MasihRawat = [int(i) for i in MasihRawat] # ubah menjadi integer
    
    # ambil data Sembuh yang berada di tag 'th' tanpa atribut class
    findSembuh = table.findAll('th', attrs={'class':None})
    Sembuh = [] # buat list kosong yang akan menyimpan Sembuh tiap kecamatan
    # lakukan looping tiap kecamatan yang akan mengambil semua Sembuh per kecamatan
    # data Sembuh berada mulai dari index ke-18 seterusnya dengan kelipatan 19,
    # hingga panjang variabel findSembuh dikurang 18
    for i in np.arange(18,len(findSembuh)-18,19):
        Sembuh.append(findSembuh[i].text)
    Sembuh = [int(i) for i in Sembuh] # ubah menjadi integer
    
    # tambahkan tiap list Desa yang dihasilkan tiap kecamatan menjadi sebuah gabungan list Desa-Desa
    # lakukan hal serupa pada data list yang sisanya
    listDesa.append(Desa)
    listODPjumlah.append(ODPjumlah)
    listODPmasihPantau.append(ODPmasihPantau)
    listODPkeluarSelesai.append(ODPkeluarSelesai)
    listPDPjumlahKasus.append(PDPjumlahKasus)
    listNegatif.append(Negatif)
    listPositif.append(Positif)
    listBelumKeluar.append(BelumKeluar)
    listMasihRawat.append(MasihRawat)
    listSembuh.append(Sembuh)


# In[39]:


# berhubung hasil list-list di atas masing-masing masih berbentuk list 2D,
# kita perlu mengubahnya masing-masing menjadi list 1D
# pertama, buat list-list kosong untuk menyimpan list 1D tsb
desaList = []
ODPjumlahList = []
ODPmasihPantauList = []
ODPkeluarSelesaiList = []
PDPjumlahKasusList = []
NegatifList = []
PositifList = []
BelumKeluarList = []
MasihRawatList = []
SembuhList = []

# lalu lakukan looping untuk tiap list 2D agar dapat diubah menjadi list 1D
for i, i_fill in enumerate(listDesa):
    for j, j_fill in enumerate(listDesa[i]):
        desaList.append(listDesa[i][j])
        
for i, i_fill in enumerate(listODPjumlah):
    for j, j_fill in enumerate(listODPjumlah[i]):
        ODPjumlahList.append(listODPjumlah[i][j])
        
for i, i_fill in enumerate(listODPmasihPantau):
    for j, j_fill in enumerate(listODPmasihPantau[i]):
        ODPmasihPantauList.append(listODPmasihPantau[i][j])
        
for i, i_fill in enumerate(listODPkeluarSelesai):
    for j, j_fill in enumerate(listODPkeluarSelesai[i]):
        ODPkeluarSelesaiList.append(listODPkeluarSelesai[i][j])
        
for i, i_fill in enumerate(listPDPjumlahKasus):
    for j, j_fill in enumerate(listPDPjumlahKasus[i]):
        PDPjumlahKasusList.append(listPDPjumlahKasus[i][j])
        
for i, i_fill in enumerate(listNegatif):
    for j, j_fill in enumerate(listNegatif[i]):
        NegatifList.append(listNegatif[i][j])
        
for i, i_fill in enumerate(listPositif):
    for j, j_fill in enumerate(listPositif[i]):
        PositifList.append(listPositif[i][j])
        
for i, i_fill in enumerate(listBelumKeluar):
    for j, j_fill in enumerate(listBelumKeluar[i]):
        BelumKeluarList.append(listBelumKeluar[i][j])
        
for i, i_fill in enumerate(listMasihRawat):
    for j, j_fill in enumerate(listMasihRawat[i]):
        MasihRawatList.append(listMasihRawat[i][j])
        
for i, i_fill in enumerate(listSembuh):
    for j, j_fill in enumerate(listSembuh[i]):
        SembuhList.append(listSembuh[i][j])


# In[284]:


# setelah semua list 1D didapatkan, 
# sekarang gabungkan semua list menjadi suatu list final
dataBadung = [desaList, ODPjumlahList, ODPmasihPantauList, ODPkeluarSelesaiList, PDPjumlahKasusList, 
              NegatifList, PositifList, BelumKeluarList, MasihRawatList, SembuhList]

# lalu ubah list final tsb menjadi dataframe, lalu transpose-kan
df = pd.DataFrame(dataBadung).transpose()


# In[283]:


# definisikan list yang berisi headers
headersBadung = ['TANGGAL-UPDATE', 'KABUPATEN', 'KECAMATAN', 'DESA', 'ZONA_HEXCOLOR', 'ODP-JUMLAH KASUS KUMULATIF', 'ODP-MASIH PEMANTAUAN', 
                 'ODP-KELUAR/SELESAI PEMANTAUAN', 'PDP-JUMLAH KASUS KUMULATIF', 'PDP-NEGATIF', 
                 'PDP-POSITIF', 'PDP-BELUM KELUAR HASIL', 'PDP-MASIH PERAWATAN', 'PDP-SEMBUH']


# In[42]:


# definisikan list yang berisi daftar kecamatan tiap desa 
Kecamatan = ["KUTA SELATAN", "KUTA SELATAN", "KUTA SELATAN", "KUTA SELATAN", "KUTA SELATAN", "KUTA SELATAN", 
"KUTA", "KUTA", "KUTA", "KUTA","KUTA","KUTA UTARA","KUTA UTARA","KUTA UTARA","KUTA UTARA","KUTA UTARA",
"KUTA UTARA","MENGWI","MENGWI","MENGWI","MENGWI","MENGWI","MENGWI","MENGWI","MENGWI","MENGWI","MENGWI",
"MENGWI","MENGWI","MENGWI","MENGWI","MENGWI","MENGWI","MENGWI","MENGWI","MENGWI","MENGWI","ABIANSEMAL",
"ABIANSEMAL","ABIANSEMAL","ABIANSEMAL","ABIANSEMAL","ABIANSEMAL","ABIANSEMAL","ABIANSEMAL","ABIANSEMAL",
"ABIANSEMAL","ABIANSEMAL","ABIANSEMAL","ABIANSEMAL","ABIANSEMAL","ABIANSEMAL","ABIANSEMAL","ABIANSEMAL",
"ABIANSEMAL","PETANG","PETANG","PETANG","PETANG","PETANG","PETANG","PETANG"]

# buat list yang berisi 'Badung'
Kabupaten = ['BADUNG' for i in range(df.shape[0])]


# In[251]:


# buat list yang berisi nama desa dengan urutan yang menyesuaikan dengan yang ada di map di webpage
DesaMap = ['Kedonganan', 'Tuban', 'Kuta', 'Legian', 'Seminyak', 'Dalung', 'Kerobokan', 'Kerobokan kaja', 
           'Tibubeneng', 'Canggu', 'Kerobokan kelod', 'Pecatu', 'Ungasan', 'Kutuh', 'Benoa', 'Tanjung benoa', 'Jimbaran', 
           'Baha', 'Buduk', 'Cemagi', 'Gulingan', 'Kekeran', 'Kuwum', 'Mengwi', 'Mengwitani', 'Munggu', 'Penarungan', 
           'Pererenan', 'Sembung', 'Sobangan', 'Tumbak bayuh', 'Werdi bhuwana', 'Abianbase', 'Kapal', 'Lukluk', 'Sading',
           'Sempidi', 'Darmasaba', 'Sibang gede', 'Jagapati', 'Angantaka', 'Sedang', 'Sibang kaja', 'Mekar bhuana', 
           'Mambal', 'Abiansemal', 'Dauh yeh cani', 'Ayunan', 'Blahkiuh', 'Punggul', 'Bongkasa', 'Taman', 'Selat', 
           'Sangeh', 'Bongkasa pertiwi', 'Belok/sidan', 'Pelaga', 'Petang', 'Sulangai', 'Getasan', 'Pangsan', 'Carangsari']

# lalu ubah isi list nya menjadi huruf kapital
DesaMap = [i.upper() for i in DesaMap]


# In[213]:


# masukkan alamat URL untuk scraping warna zona
url = 'https://covid19.badungkab.go.id/portal-covid'

# mulai otomasi browser menggunakan selenium
driver = webdriver.Firefox(executable_path='C:/Users/utomo/AppData/Local/Temp/webdriver/geckodriver.exe')
driver.get(url)

# dan tunggu hingga browser secara sempurna menampilkan map di webpage
wait = WebDriverWait(driver, 10)
wait.until(EC.visibility_of_all_elements_located((By.ID, "map")))
print('Map fully shown.')

# scroll ke bawah sebanyak 3500 pixel
driver.execute_script("window.scrollTo(0, 3500)") 

# tunggu 1 detik agar webpage merespon
driver.implicitly_wait(1)

# definisikan xpath yang akan digunakan sebagai posisi untuk diklik oleh selenium
# kita perintahkan selenium untuk men-close popup window yang cukup mengganggu di webpage
# hal ini diperlukan untuk meminimalkan kemungkinan error pada selenium
driver.find_element_by_xpath('//button[@class="btn btn-close"][text()="[X] Tutup"]').click()

# lempar hasil selenium ke BeautifulSoup
soupSelenium = BeautifulSoup(driver.page_source, 'html5lib')

# matikan browser karena sudah tidak dibutuhkan lagi
driver.close()

# ambil konten map yang berada di tag 'path' dengan atribut class 'leaflet-interactive'
mapInteractive = soupSelenium.findAll('path', attrs={'class':'leaflet-interactive'})

# ambil data mengenai warna tiap peta kecamatan
# warna tsb mengindikasi zona tiap kecamatan
# data warna tsb berada di dalam atribut 'fill'
fillList = [] # buat list kosong yang akan menyimpan data atribut 'fill'
for i in mapInteractive:
    fillList.append(i.get('fill'))
    
# berhubung webpage juga memasukkan peta kecamatan yang bukan merupakan bagian dari Badung,
# kita perlu membuang peta kecamatan non-Badung tersebut
# semua peta kecamatan non-Badung memiliki warna putih
# dalam kode warna hex, warna putih berkode #ffffff,
# sehingga kita cukup membuang semua atribut 'fill' yang berkode tsb
Color = []
for i, j in enumerate(fillList):
    if j != '#ffffff':
        Color.append(j)


# In[252]:


# gabung list DesaMap dan Color sehingga menjadi sebuah dictionary
DesaColorDict = dict(zip(DesaMap, Color))


# In[247]:


# buat function yang akan memetakan warna dengan desanya di dataframe
def fitZone(x):
    global DesaColorDict
    for key, value in DesaColorDict.items():
        if x in key:
            return(value)


# In[281]:


# buat list yang berisi hasil pemetaan antara warna dengan urutan nama desa di dataframe
Zona_HexColor = list(map(fitZone, df[0]))


# In[262]:


# buat kolom Tanggal yang mana data tanggalnya didapatkan dari informasi di website
# informasi tanggal berada di tag 'p' dengan atribut class 'text-center'
TanggalRaw = soupSelenium.find('p', class_='text-center').text

# lalu bersihkan tanggal dari characters yang mengganggu
idxToGetDate = TanggalRaw.find(',')+2
Tanggal = TanggalRaw[idxToGetDate:]
# lalu ubah menjadi list
Tanggal = [Tanggal for i in range(len(Kecamatan))]


# In[285]:


# masukkan list Tanggal, Kabupaten, Kecamatan, dan Zona_HexColor,
# ke dalam dataframe dengan index masing2 0,1,2,4
# lalu namai masing-masing
df.insert(0, column='TANGGAL-UPDATE', value=Tanggal)
df.insert(1, column='KABUPATEN', value=Kabupaten)
df.insert(2, column='KECAMATAN', value=Kecamatan)
df.insert(4, column='ZONA_HEXCOLOR', value=Zona_HexColor)

# set header-nya
df.columns = headersBadung


# In[286]:


# definisikan sebuah dictionary yang berisi kode hex warna dengan nama warna zonanya
NamaWarnaDict = {'#FF9800':'Jingga',
                 '#FFC107':'Kuning',
                 '#FF5252':'Merah',
                 '#4CAF50':'Hijau'}


# In[287]:


# buat function yang akan memetakan kode warna hex menjadi nama warna
def fitColor(x):
    global NamaWarnaDict
    for key, value in NamaWarnaDict.items():
        if x in key:
            return(value)


# In[288]:


# buat list yang berisi hasil pemetaan antara urutan kode hex warna dengan nama warnanya
Zona_Warna = list(map(fitColor, df['ZONA_HEXCOLOR']))

# lalu masukkan ke dalam dataframe dengan index 5, dan namai kolomnya
df.insert(5, column='ZONA_WARNA', value=Zona_Warna)

now = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
TanggalWaktuScrape = [now for i in range(df.shape[0])]

df.insert(1, column='TANGGAL-WAKTU-SCRAPE', value=TanggalWaktuScrape)

url = 'https://covid19.badungkab.go.id/'
SourceLink = [url for i in range(df.shape[0])]
df.insert(df.shape[1], column='Source Link', value=SourceLink)

print(df.head())


# In[11]:


# export dataframe ke csv file
df.to_csv(r'B:\Projects\Work\Covid-19\Data Scraping Bali\Badung_' + Tanggal[0] + '.csv')


# In[ ]:




