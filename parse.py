import requests
from bs4 import BeautifulSoup
import pandas as pd

url="https://www.makita.ru/products.html"
res = requests.get(url)
soup = BeautifulSoup(res.text, 'lxml')

# На входе ссылка на исходную страницу, на выходе - страницы расположенные на исходной странице.
# At the entrance, a link to the original page, at the exit - the pages located on the original page.
def links(i): 
    rezult = []
    for line in (str(i).split("<")):
        if (line.find('a href=')) >=0:
            rez=""
            for symbol in line.replace("a href=\"",""):
                if symbol=="\"":
                    break
                rez=rez+symbol
            rezult.append(rez)
    return(rezult)




# Поиск внутренних подразделов сайта с вложенными внутри товарами.
# Search for internal subsections of the site with nested products inside.
tot=[] # Список ссылок на страницы с вложенными внутри товарами. List of links to pages with nested products.
for i in (links(soup.findAll('div', class_='content tile'))):
    url="https://www.makita.ru/"+i
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')
    for i1 in (links(soup.findAll('div', class_='content tile'))):
        url="https://www.makita.ru/"+i1
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'lxml')
        for i2 in (links(soup.findAll('div', class_='content tile'))):
            url = "https://www.makita.ru/" + i2
            res = requests.get(url)
            soup = BeautifulSoup(res.text, 'lxml')
            for f in (links(soup.findAll('div', class_='content tile'))):
                url = "https://www.makita.ru/" + f
                tot.append(url)

# Заполнение массива ссылками на продукт.
# Filling the array with links to the product.
href=[] # Ссылки на товары. Links to goods.
for url in tot:
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')
    rez = []
    for i in (soup.findAll('div', class_='product-number')):
        stri=""
        for symbol in ((str(i).split('href=\"'))[1]):
            if symbol=="\"":
                break
            stri=stri+symbol
        rez.append(stri)
    href.append(rez)

    
text=[] # Описание товара
urls=[] # Ссылка на товар
productnumbers=[] # Код товара

# Осмотр страниц товара, берется основная информация для товара.
# Inspection of product pages, basic information for the product is taken.
for i1 in (list(filter(None, href))):
    for i in (list(filter(None, i1))):
        url = "https://www.makita.ru/" + i
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'lxml')

        urls.append(url)
        productnumbers.append((str(soup.findAll('span', class_='product-number'))).replace("[<span class=\"product-number\">","").replace("</span>]",""))
        text.append((str(soup.findAll('div', class_='product-description--marketing-text'))).replace("[<div class=\"product-description--marketing-text\">","").replace("</div>]",""))

print(text)
print(urls)
print(productnumbers)

df = pd.DataFrame({'URL': urls,'PRODUCTNUMBERS': [productnumbers],'DESCRIPTION': [text]})
df.to_excel('./base.xlsx')
