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

# masukkan alamat URL
url = 'http://infocorona.tabanankab.go.id/'

# mulai otomasi browser menggunakan selenium
driver = webdriver.Firefox(executable_path='C:/Users/utomo/AppData/Local/Temp/webdriver/geckodriver.exe')
driver.get(url)

# dan tunggu hingga browser secara sempurna menampilkan tabel yang akan di-scrape
wait = WebDriverWait(driver, 10)
wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "card")))
print('ready to scrape.') # siap mulai scraping

# lempar hasil otomasi browser ke BeautifulSoup untuk di-scrape
soupTabanan = BeautifulSoup(driver.page_source, 'html5lib')

# ambil tag dari daftar Kecamatan di tabel
# Kecamatan berada di tag 'ul' dengan atribut class 'nav nav-tabs'
TabKec = soupTabanan.find('ul', attrs={'class':'nav nav-tabs'})
# TabKec

# lebih detailnya, Kecamatan berada di dalam tag 'li'.
# ambil isi teks dari tag tsb
Kecamatan = []
for i in TabKec.findAll('li'):
    Kecamatan.append(i.text)
# Kecamatan

# ambil headers
# headers berada di tag 'div' dengan atribut class 'tab-content',
# lalu di dalam tag 'div' dengan atribut class 'tab-pane show vivify fadeIn active',
# lalu di dalam tag 'th'
headers = []

table = soupTabanan.find('div', attrs={'class':'tab-content'}).find('div', attrs={'class':'tab-pane show vivify fadeIn active'})
for i in table.findAll('th')[1:5]:
    headers.append(i.text)
    
headers.insert(0, 'KECAMATAN') # berhubung di headers tidak terdapat kolom Kecamatan, tambahkanlah secara manual

# buat list sebagai tempat penyimpanan final konten dari tabel
dataTabanan = []

# mulai looping menggunakan selenium untuk mengklik tiap tab di tabel,
# lalu melempar hasil html-nya ke BeautifulSoup untuk di-scrape.
# lakukan loop sebanyak jumlah tab, yaitu jumlah Kecamatan
for j in range(len(Kecamatan)):
    # definisikan xpath yang akan digunakan sebagai posisi untuk diklik oleh selenium
    # berhubung tiap tab memiliki xpath yang mirip, jadi hanya di bagian 'Kecamatan[j]' nya saja yang diganti tiap loop
    xpath = '//a[@data-toggle="tab"][text()="' + Kecamatan[j] + '"]'
    
    # perintahkan selenium untuk mengklik tab dengan menggunakan xpath yang telah diberikan
    cursor = driver.find_element_by_xpath(xpath)
    cursor.click()
    
    # tunggu 1 detik agar tab yang telah diklik merespon
    driver.implicitly_wait(1)
    
    # lempar hasil klik ke BeautifulSoup
    soupPerTab = BeautifulSoup(driver.page_source, 'html5lib')
    
    # ambil isi tabel yang ingin di-scrape.
    # isi tabel berada di tag 'div' dengan atribut class 'tab-content',
    # lalu di dalam tag 'div' dengan atribut class 'tab-pane show vivify fadeIn active'
    table = soupPerTab \
        .find('div', attrs={'class':'tab-content'}) \
        .find('div', attrs={'class':'tab-pane show vivify fadeIn active'})
    
    # buat variabel sequence sebagai looping untuk tiap isi kolom di dalam tabel hasil scraped
    seqNamaDesa = np.arange(1, len(table.findAll('td')), 5)
    seqJMLOTG = np.arange(2, len(table.findAll('td')), 5)
    seqJMLODP = np.arange(3, len(table.findAll('td')), 5)
    seqJMLPDP = np.arange(4, len(table.findAll('td')), 5)
    
    # buat variabel list kosong sebagai penyimpan hasil tiap kolom
    NamaDesa = []
    JMLOTG = []
    JMLODP = []
    JMLPDP = []
    
    # mulai lakukan looping untuk mengambil isi dari Desa, OTG, ODP, dan PDP
    for i in seqNamaDesa:
        NamaDesa.append(table.findAll('td')[i].text)
    for i in seqJMLOTG:    
        JMLOTG.append(table.findAll('td')[i].text)
    for i in seqJMLODP:    
        JMLODP.append(table.findAll('td')[i].text)
    for i in seqJMLPDP:    
        JMLPDP.append(table.findAll('td')[i].text)
        
    # pindahkan isi dari hasil looping di atas ke list yang menampung semuanya
    dataTabanan_temp = [[Kecamatan[j] for i in range(len(NamaDesa))], # buat list yang berisi nama-nama Kecamatan
                        NamaDesa,
                        JMLOTG,
                        JMLODP,
                        JMLPDP]
    dataTabanan.append(dataTabanan_temp)
    
# cek apakah benar ukuran list yang telah didapatkan adalah 10x5
print('Apakah ukuran list 10x5?', np.array(dataTabanan).shape == (10,5))

# matikan browser karena sudah tidak dibutuhkan lagi
driver.close()

# buat list 1D berisi daftar nama kecamatan untuk tiap desa
# daftar ini diekstrak dari list dataTabanan yg berukuran 3D
Kec_temp = [dataTabanan[i][0] for i in range(len(dataTabanan))]
i = 0
Kec = []
while i < len(Kec_temp):
    Kec += Kec_temp[i]
    i += 1
    
# buat list 1D berisi daftar nama desa
# daftar ini diekstrak dari list dataTabanan yg berukuran 3D
Desa_temp = [dataTabanan[i][1] for i in range(len(dataTabanan))]
i = 0
Desa = []
while i < len(Desa_temp):
    Desa += Desa_temp[i]
    i += 1
    
# buat list 1D berisi daftar OTG
# daftar ini diekstrak dari list dataTabanan yg berukuran 3D
JMLOTG_temp = [dataTabanan[i][2] for i in range(len(dataTabanan))]
i = 0
JMLOTG = []
while i < len(JMLOTG_temp):
    JMLOTG += JMLOTG_temp[i]
    i += 1
    
# buat list 1D berisi daftar ODP
# daftar ini diekstrak dari list dataTabanan yg berukuran 3D
JMLODP_temp = [dataTabanan[i][3] for i in range(len(dataTabanan))]
i = 0
JMLODP = []
while i < len(JMLODP_temp):
    JMLODP += JMLODP_temp[i]
    i += 1
    
# buat list 1D berisi daftar PDP
# daftar ini diekstrak dari list dataTabanan yg berukuran 3D
JMLPDP_temp = [dataTabanan[i][4] for i in range(len(dataTabanan))]
i = 0
JMLPDP = []
while i < len(JMLPDP_temp):
    JMLPDP += JMLPDP_temp[i]
    i += 1
    
# setelah semua list 1D didapatkan, buatlah menjadi dataframe, lalu transpose dataframe-nya
df = pd.DataFrame([Kec, Desa, JMLOTG, JMLODP, JMLPDP]).transpose()

# set headers nya
df.columns = headers
# df.head()

# buat kolom Tanggal yang mana data tanggalnya didapatkan dari informasi di website
# informasi tanggal berada di tag 'div' dengan atribut class 'card-header', dan berada di urutan kedua
# lalu berada di dalam atribut 'p'
tanggalRaw = soupTabanan.findAll('div', class_='card-header')[2].find('p').text

# setelah data raw tanggal didapatkan, bersihkan data tersebut dari character yang mengganggu
Tanggal = tanggalRaw[tanggalRaw.find(':')+2:]
# lalu buat menjadi sebuah list
Tanggal = [Tanggal for i in range(df.shape[0])]

# code di bawah ini digunakan jika anda ingin membuat list Tanggal dari informasi tanggal hari ini
# Tanggal = [datetime.date.today() for i in range(df.shape[0])]

# masukkan data tanggal ke kolom di index ke-0, dan namai kolomnya dengan'TANGGAL-UPDATE'
df.insert(0, column='TANGGAL-UPDATE', value=Tanggal)
# df.head()

# buat sebuah list yang berisi 'Tabanan'
Kab = ['Tabanan' for i in range(df.shape[0])]
# masukkan data Kabupaten ke kolom di index ke-1, dan namai kolomnya dengan'KABUPATEN'
df.insert(1, column='KABUPATEN', value=Kab)

now = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
TanggalWaktuScrape = [now for i in range(df.shape[0])]

df.insert(1, column='TANGGAL-WAKTU-SCRAPE', value=TanggalWaktuScrape)

SourceLink = [url for i in range(df.shape[0])]
df.insert(df.shape[1], column='Source Link', value=SourceLink)

print(df)

# export dataframe ke file csv
df.to_csv(r'B:\Projects\Work\Covid-19\Data Scraping Bali\Tabanan_' + Tanggal[0] + '.csv')