#!/usr/bin/env python
# coding: utf-8

# In[1]:


# import semua library yang diperlukan
import pandas as pd
import numpy as np
import re
from bs4 import BeautifulSoup
import html5lib
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import matplotlib.pyplot as plt
import matplotlib.path as mplPath
import datetime

# In[2]:


# masukkan alamat URL
url = 'http://infocovid19.bulelengkab.go.id/'


# In[4]:


# mulai otomasi browser menggunakan selenium
driver = webdriver.Firefox(executable_path='C:/Users/utomo/AppData/Local/Temp/webdriver/geckodriver.exe')
driver.get(url)

# dan tunggu hingga browser secara sempurna menampilkan map di webpage
wait = WebDriverWait(driver, 10)
wait.until(EC.visibility_of_all_elements_located((By.ID, "mapid")))
print('ready to scrape.') # siap mulai scraping


# In[5]:


# scroll ke bawah sebanyak 1080 pixel.
driver.execute_script("window.scrollTo(0, 1080)")


# In[6]:


# lempar hasil selenium ke BeautifulSoup
soupBuleleng = BeautifulSoup(driver.page_source, 'html5lib')


# In[7]:


# matikan browser karena sudah tidak dibutuhkan lagi
driver.close()


# In[8]:


# ambil data koordinat dari peta yang digambarkan oleh webpage
# data ini berada di tag 'path' dengan atribut class 'leaflet-interactive',
# lalu ambil isi dari atribut 'd'
dList = [] # buat list kosong yang akan menyimpan isi atribut 'd'
for i in soupBuleleng.findAll('path', class_='leaflet-interactive'):
    dList.append(i.get('d'))


# In[9]:


# atribut 'd' ini berisi posisi koordinat x dan y
# koordinat x berada setelah sebuah huruf M atau L
# koordinat y berada setelah sebuah spasi dan/atau sebelum huruf L atau z
X = [] # buat list kosong yang akan menyimpan isi koordinat x
Y = [] # buat list kosong yang akan menyimpan isi koordinat y
# jadi, list X akan menyimpan list koor x dari tiap kecamatan,
# sedangkan list Y akan menyimpan list koor y dari tiap kecamatan

# lakukan looping ke dalam variabel dList untuk mengambil koor x dan y
for j, j_fill in enumerate(dList):
    x = []
    for i in re.findall('M{1}\d+|L{1}\d+', j_fill):
        x.append(int(i[1:]))
    x.append(x[0])
#     print(len(x))

    y = []
    for i in re.findall('-*\d+(?:L|z)', j_fill):
        y.append(int(i[:-1]))
    y.append(y[0])
#     print(len(y))
    
    X.append(x)
    Y.append(y)
    
# print(X)
# print(Y)


# In[28]:


# ambil data mengenai pin marker yang menandai jumlah OTG, ODP, PDP, Positif pada map
# data pin tsb berada di tag 'div' dengan atribut class 'leaflet-marker-icon'
styleList = [] # buat list kosong yang akan menyimpan data atribut style (isinya ada koor pin)
numList = [] # buat list kosong yang akan menyimpan konten jumlah OTG, ODP, dst
tipeList = [] # buat list kosong yang akan menyimpan jenis pin apakah pin OTG, ODP, dst

# mulai loopin
for i in soupBuleleng.findAll('div', class_='leaflet-marker-icon'):
    # style berada di dalam atribut 'style'
    styleList.append(i.get('style')) 
    
    # jumlah OTG, ODP, dst berada di tag 'div' dengan atribut class 'number'
    numList.append(int(i.find('div', class_='number').text))
    
    # buat variabel sementara bernama tipe yang mengambil isi dari tag 'img' dari dalam atribut 'src'
    tipe = i.find('img').get('src')
    # berhubung isi atribut 'src' adalah sebuah link ke file png, 
    # kita bersihkan isinya agar mendapatkan jenis yang diinginkan, yaitu apakah OTG, ODP, dst
    tipe = re.findall('\w+\.p', tipe)[0][:-2]
    tipeList.append(tipe)


# In[14]:


# dari list styleList di atas, kita bisa mendapatkan koor dari tiap pin marker
x_coor = [] # buat list kosong yang akan menyimpan x koor pin
y_coor = [] # buat list kosong yang akan menyimpan y koor pin

# mulai looping ke dalam list styleList
for i in styleList:
    # kedua koor tersebut berada di dalam fungsi 'translate3d()',
    # sehingga perlu dipisahkan
    xy = re.findall('\(\d+px,\s\d+px', i)[0][1:]
    x_coor.append(int(xy[:(xy.find('px,'))]))
    y_coor.append(int(xy[(xy.find(',')+2):-2]))


# In[16]:


# buat plotting dari koordinat kecamatan dan koordinat pin marker yang telah didapatkan
# hal ini semata-mata hanya untuk melihat hasil extract data
plt.figure(figsize=(10,6))
for i in range(len(x_coor)):
    if i <= 8:
        plt.plot(X[i], Y[i], 'go--', linewidth=1, markersize=1)
        
    
    plt.plot(x_coor[i], y_coor[i], 'bo--', linewidth=1, markersize=5)

plt.grid(True)


# In[32]:


# menguji apakah lokasi tiap pin marker berada di dalam sebuah area kecamatan
# jika BENAR sebuah pin marker berada di sebuah area kecamatan,
# maka segala atribut (tipe pin dan jumlah penederita) pin marker tsb menjadi milik kecamatan tsb
# jika TIDAK, maka kecamatan tsb tidak memiliki pin tsb
jumlahPerKec = [] # buat list kosong untuk menyimpan jumlah penderita tiap kecamatan
tipePerKec = [] # buat list kosong untuk menyimpan tipe penderita tiap kecamatan

# mulai looping sebanyak jumlah kecamatan, dalam hal ini sebanyak panjang koor X
for i in range(len(X)):
    # ubah koordinat x dan y tiap kecamatan menjadi sebuah array
    # hal ini diperlukan mengingat fungsi Path pada matplotlib hanya menerima array
    KecArray = np.array([[X[i][j],Y[i][j]] for j in range(len(X[i]))])
    
    jumlah = [] # buat list kosong yang akan menampung data jumlah pada tiap kecamatan
    tipe = [] # buat list kosong yang akan menampung data tipe pada tiap kecamatan
    
    # buat polygon dengan menggunakan koordinat tiap kecamatan,
    mapPath = mplPath.Path(KecArray)
    
    # lalu pada tiap kecamatan, lakukan looping semua jumlah pin marker
    for k in range(len(x_coor)):
        # tentukan koor x dan y tiap pin marker
        pin = (x_coor[k], y_coor[k])
        
        # ambil hasil boolean dari apakah pin berada di dalam polygon kecamatan
        isInside = mapPath.contains_point(pin)
        # jika BENAR berada di dalam, maka tambahkan semua atribut pin tersebut ke dalam kecamatan ybs
        if isInside:
            jumlah.append(numList[k])
            tipe.append(tipeList[k])
            
    jumlahPerKec.append(jumlah)
    tipePerKec.append(tipe)


# In[33]:


tipePerKec


# In[34]:


# definisikan nama-nama kecamatan secara manual
# urutan nama-nama ini menyesuaikan dengan urutan muncul di webpage
Kecamatan = ['Sawan', 'Gerokgak', 'Banjar', 'Buleleng', 'Busungbiu', 'Kubutambahan', 'Seririt', 'Sukasada', 'Tejakula']


# In[35]:


# definisian headers secara manual
headers = ['KECAMATAN', 'POSITIF', 'PDP', 'ODP', 'OTG']


# In[36]:


# setelah data kepemilikan tiap pin marker pada tiap kecamatan didapatkan,
# sekarang saatnya memisahkan data tersebut agar menjadi 4 buah list,
# yaitu OTG, ODP, PDP, dan Positif
# jika sebuah kecamatan hanya memiliki beberapa tipe penderita (yaitu hanya OTG saja atau hanya OTG dan PDP, dsb),
# maka data penderita yang nihil tersebut akan diisi 0.
# begitu pula jika sebuah kecamatan sama sekali tidak memiliki pin marker,
# maka semua list OTG, ODP, dst diisi 0.
OTG = [] # buat list kosong yang akan menyimpan data OTG
ODP = [] # buat list kosong yang akan menyimpan data ODP
PDP = [] # buat list kosong yang akan menyimpan data PDP
Positif = [] # buat list kosong yang akan menyimpan data Positif

# lakukan looping sebanyak panjang list tipePerKec
for i in range(len(tipePerKec)):
    # jika kecamatan memiliki setidaknya 1 satu tipe penderita:
    if tipePerKec[i]:
        # buat variabel kosong sebagai buffer penyimpanan sementara sebelum diisi ke list
        otg = 0
        odp = 0
        pdp = 0
        positif = 0
        
        # lalu lakukan looping ke dalam isi kecamatan
        for j in range(len(tipePerKec[i])):
            
            # jika terdapat 'otg', maka set variabel otg
            if 'otg' in tipePerKec[i][j]:
                otg = jumlahPerKec[i][j]
            
            # atau jika terdapat 'odp', maka set variabel odp
            elif 'odp' in tipePerKec[i][j]:
                odp = jumlahPerKec[i][j]
            
            # jika terdapat 'pdp', maka set variabel pdp
            elif 'pdp' in tipePerKec[i][j]:
                pdp = jumlahPerKec[i][j]
                
            # jika terdapat 'positif', maka set variabel positif
            elif 'positif' in tipePerKec[i][j]:
                positif = jumlahPerKec[i][j]
        
        # setelah loop isi sebuah kecamatan selesai,
        # lakukan pengujian apakah variabel buffer otg, odp, dst memiliki nilai 0
        # jika TIDAK 0, maka append list ybs dengan isinya
        # jika BENAR 0, maka append list ybs dengan nilai 0
        if otg != 0:
            OTG.append(otg)
        else:
            OTG.append(0)
            
        if odp != 0:
            ODP.append(odp)
        else:
            ODP.append(0)
            
        if pdp != 0:
            PDP.append(pdp)
        else:
            PDP.append(0)
            
        if positif != 0:
            Positif.append(positif)
        else:
            Positif.append(0)
    
    # jika kecamatan sama sekali tidak memiliki pin marker:
    else:
        OTG.append(0)
        ODP.append(0)
        PDP.append(0)
        Positif.append(0)


# In[37]:


# lalu gabung semua list
dataBuleleng = [Kecamatan,
               OTG,
               ODP,
               PDP,
               Positif]


# In[38]:


# ubah list gabungan tsb menjadi dataframe
df = pd.DataFrame(dataBuleleng).transpose()
# set header nya
df.columns = headers


# In[39]:


# buat kolom Tanggal dan Waktu yang mana data tanggal waktunya didapatkan dari informasi di website
# informasi tanggalwaktu berada di tag 'div' dengan atribut class 'container py-3',
# lalu di dalam tag 'h6'
TanggalWaktuRaw = soupBuleleng.find('div', class_='container py-3').find('h6').text

# lalu bersihkan tanggalwaktu dari characters yang mengganggu
TanggalWaktu = re.findall('\d+\s\w+\s\d{4},\s\d{2}\:\d{2}\:\d{2}\sWITA', TanggalWaktuRaw)[0]

# lalu pisahkan variabel tanggalwaktu menjadi tanggal dan waktu
Tanggal = TanggalWaktu[:TanggalWaktu.find(',')]
Waktu = TanggalWaktu[TanggalWaktu.find(',')+2:]


# In[40]:


# buat list yang berisi nama kabupaten
Kabupaten = ['Buleleng' for i in range(df.shape[0])]

# buat list tanggal dari variabel tanggal di atas
Tanggal = [Tanggal for i in range(df.shape[0])]
# buat list waktu dari variabel waktu di atas
Waktu = [Waktu for i in range(df.shape[0])]


# In[42]:


# ambil data mengenai warna tiap peta kecamatan
# warna tsb mengindikasi zona tiap kecamatan
# data warna tsb berada di tag 'path' dengan atribut class 'leaflet-interactive',
# lalu di dalam atribut 'fill'
fillList = [] # buat list kosong yang akan menyimpan data atribut 'fill'
for i in soupBuleleng.findAll('path', class_='leaflet-interactive'):
    fillList.append(i.get('fill'))


# In[43]:


# definisikan sebuah dictionary yang berisi kode hex warna dengan nama warna zonanya
NamaWarnaDict = {'#6AA8DB':'Biru-OTG',
                 '#ED5752':'Merah-Positif',
                 '#FCDE77':'Kuning-ODP',
                 '#61B889':'Hijau-Bersih'}


# In[44]:


# buat function yang akan memetakan kode warna hex menjadi nama warna
def fitColor(x):
    global NamaWarnaDict
    for key, value in NamaWarnaDict.items():
        if x in key:
            return(value)


# In[45]:


# buat list yang berisi hasil pemetaan antara urutan kode hex warna dengan nama warnanya
Zona_Warna = list(map(fitColor, fillList))


# In[46]:


# masukkan list Tanggal, Waktu, Kabupaten, fillList, dan Zona-Warna,
# ke dalam dataframe dengan index masing2 0,1,2,4,5,
# lalu namai masing-masing
df.insert(0, column='TANGGAL-UPDATE', value=Tanggal)
df.insert(1, column='WAKTU-UPDATE', value=Waktu)
df.insert(2, column='KABUPATEN', value=Kabupaten)
df.insert(4, column='ZONA_WARNA_HEX', value=fillList)
df.insert(5, column='ZONA_WARNA', value=Zona_Warna)


# In[ ]:

now = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
TanggalWaktuScrape = [now for i in range(df.shape[0])]

df.insert(2, column='TANGGAL-WAKTU-SCRAPE', value=TanggalWaktuScrape)

SourceLink = [url for i in range(df.shape[0])]
df.insert(df.shape[1], column='Source Link', value=SourceLink)

print(df)


# In[ ]:


# export dataframe ke file csv
df.to_csv(r'B:\Projects\Work\Covid-19\Data Scraping Bali\Buleleng_' + Tanggal[0] + '.csv')

