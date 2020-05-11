# Scraping Covid-19 Websites

This repo contains py scripts to scrape information regarding Covid-19 in Bali province and its regencies.

The websites which are scraped are the following:

https://infocorona.baliprov.go.id/
https://covid19.badungkab.go.id
http://covid19.banglikab.go.id
http://infocovid19.bulelengkab.go.id/
https://covid19.gianyarkab.go.id
http://covid19.jembranakab.go.id
http://infocorona.karangasemkab.go.id/
http://covid19.klungkungkab.go.id
http://infocorona.tabanankab.go.id
https://covid19.denpasarkota.go.id

Each website use different user interface. Therefore, in order to scrape it, I also use different technique. Some use BeautifulSoup only; some use BeautifulSoup and Selenium; and there is one (Buleleng website) that uses matplotlib to scrape the numeric data which are embedded inside a map.

