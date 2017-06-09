# Opengazettes Nigeria Scraper
[SCRAPY] Nigerian Gazettes obtained from the Centre for Research Libraries Global Resources Network (https://dds.crl.edu/crldelivery/27040)

# Getting Started
Clone this repo by running:
```
$ git clone https://github.com/CodeForAfrica-SCRAPERS/opengazettes_ng_scrapy.git
```

Install the requirements from the `requirements.txt` file:
```
$ pip install -r requirements.txt
```

Crawl Nigerian gazettes for a specific year by running:
```
$ scrapy crawl ng_gazettes -a year=1971
```
At the time of writing, the years with gazettes available are years:
`1957-1964` , `1967-1971`, and `1973-1974`

Here's a screenshot showing what the scraper does. 
![Nigeria Gazette Scraper](https://lh5.googleusercontent.com/IWxSjBgcqBslv2fHKM-DFjvA_URBlhuOIbEHgDNyArPuWAaxQ4OoHKdJcX7zDTIa0nuXLtB7Me15u2c=w2402-h1188-rw)
