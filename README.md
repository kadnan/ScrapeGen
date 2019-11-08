# ScrapeGen

_ScrapeGen_ is a simple tool written in python that generates the code of a web scraper based on rules given in a file.


## Why was it created?
 
No particular reasons other than I was bored and I had come across Simone Giertz's TED talk [Why you should make useless things](https://www.ted.com/talks/simone_giertz_why_you_should_make_useless_things?language=en), hence thought to create something useless.

## How it works?
This tool generate a parser that basically rely on Python `requests` and `Beautifulsoup`. If I got bored again then I might add other libraries too, who knows?

Anyways, you will create a YAML file first that will contain all info about the parser. A typical YAML file that generates a parser will look like below:

```
script_name: olx_indi_test.py # Name of the scraper file
main: # Code under _main_ function
  entry_url: https://www.olx.com.pk/item/1-kanal-brand-bew-banglow-available-for-sale-in-wapda-town-iid-1009971253 # URL to be parsed
  entry_function: parse # The function that uses requests library to fetch the data and calling Bs4

rules: # Each Selector will be a separate rule that itself will be a separate method
    - name: price
      type: single #Valid types: array,single
      selector: '#container > main > div > div > div.rui-2SwH7.rui-m4D6f.rui-1nZcN.rui-3CPXI.rui-3E1c2.rui-1JF_2 > div.rui-2ns2W._2r-Wm > div > section > span._2xKfz'
      extract: #Either an attribute value or just text
        what: text

    - name: seller
      type: single #Valid types: array,single
      selector: '#container > main > div > div > div.rui-2SwH7.rui-m4D6f.rui-1nZcN.rui-3CPXI.rui-3E1c2.rui-1JF_2 > div.rui-2ns2W.YpyR- > div > div > div._1oSdP > div > a > div'
      extract:
        what: text


```

Assuming you installed all required libs mentioned in `requirements.txt`, all you have to do is to run the command:
 
 `python parse_gen.py indi.yaml` 
 
 Where `indi.yaml` is the file that contains the content given above. If it runs successfully, it generates a file with name `olx_indi_test.py` which looks like below:
 
 ```
 import requests
from bs4 import BeautifulSoup


def get_price(soup_object):
    _price = None
    price_section = soup_object.select(
        "#container > main > div > div > div.rui-2SwH7.rui-m4D6f.rui-1nZcN.rui-3CPXI.rui-3E1c2.rui-1JF_2 > div.rui-2ns2W._2r-Wm > div > section > span._2xKfz")

    if len(price_section) > 0:
        _price = price_section[0].text.strip()
    return _price


def get_seller(soup_object):
    _seller = None
    seller_section = soup_object.select(
        "#container > main > div > div > div.rui-2SwH7.rui-m4D6f.rui-1nZcN.rui-3CPXI.rui-3E1c2.rui-1JF_2 > div.rui-2ns2W.YpyR- > div > div > div._1oSdP > div > a > div")

    if len(seller_section) > 0:
        _seller = seller_section[0].text.strip()
    return _seller


def parse(_url):

    r = requests.get(_url)
    if r.status_code == 200:
        html = r.text.strip()
        soup = BeautifulSoup(html, 'lxml')
        price = get_price(soup)
        seller = get_seller(soup)


if __name__ == '__main__':
    main_url = "https://www.olx.com.pk/item/1-kanal-brand-bew-banglow-available-for-sale-in-wapda-town-iid-1009971253"
    parse(main_url)
 ```
 
 The generated can easily be modified based on your needs.  