#!/usr/bin/python3



#from urllib2 import urlopen
#import urllib2
from bs4 import BeautifulSoup
from requests_html import AsyncHTMLSession
import asyncio
import sys

URL = "https://www.thegreatcourses.com/courses/language-and-the-mind"
#URL = "https://www.youtube.com/playlist?list=PLm-NYu03DbMtQk_QdGvIaI31AtUlIB8Kq"
#USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0'

headers = {'user-agent': USER_AGENT, 'timeout' : '50000'}


async def process_links():
    asession = AsyncHTMLSession()
    r =  await asession.get(URL)
    results = await r.html.arender(retries=4, timeout=1000)
    sel = 'html.hiddenHeader body div#root.page-wrapper main.ProductPage div.container div.ProductPage-PageContent'
    title = r.html.find(sel, first=True)
    print(results)
    await asession.close()
    
 

'''
session = HTMLSession()
#session.set_header('User-Agent', USER_AGENT)

r = await session.get(URL, headers=headers)

r =  await r.html.render()  # this call executes the js in the page
ProfessorName = r.absolute_links


print(ProfessorName) 
'''
asyncio.run(process_links())