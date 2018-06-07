#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import jsonlines
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

def get_generos(endereco):
    html = get_html(endereco)
    soup = BeautifulSoup(html,"lxml")
    generos = set()

    for genero in soup.find_all("img",alt=True):
        generos.add(genero["alt"])
    return generos

def get_html(url_site):
    req = requests.get(url_site)
    return req.text


def get_title_rating(genero):
    pagina = 1
    titulos = list()
    while (pagina <= 10):
        end1 = "https://www.imdb.com/search/title?genres="
        end2 = "&sort=user_rating,desc&view=simple&page="
        endereco = end1+genero+end2+str(pagina)
        html = get_html(endereco)
        soup = BeautifulSoup(html,"lxml")
        for span in soup.find_all("span",title=True):
            titulos.append(span.find("a").text)
        pagina = pagina + 1
    return titulos

    


generos = get_generos("https://www.imdb.com/feature/genre")
titulos_comedia = get_title_rating("comedy")

for genero in generos:
    fo = open("genero_"+genero+".txt", "wb")
    for titulo in titulos_comedia:
        writer = jsonlines.Writer(fo)
        writer.write(titulo)
    writer.close()
    fo.close()



    
