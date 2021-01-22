#!/usr/bin/python2



#from urllib2 import urlopen
#import urllib2
from bs4 import BeautifulSoup
import sys
import os  
import time
import random
import re
import textwrap
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from pyvirtualdisplay import Display

firefox_binary = FirefoxBinary(os.path.abspath("/usr/local/bin/firefox/firefox"))
firefox_binary.add_command_line_options('--headless')
gecko_binary = os.path.abspath("/usr/local/bin/geckodriver")
display = Display(visible=0, size=(1366, 768))
display.start()

options = Options()
options.headless = True
profile = webdriver.FirefoxProfile()
profile.set_preference("javascript.enabled", True)
#profile = webdriver.FirefoxProfile()
#profile.set_preference("javascript.enabled", True)
#profile.set_preference("general.useragent.override", "Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0")
#profile.set_preference("headless", True)
#driver = webdriver.Firefox(profile, executable_path=os.path.abspath("/usr/local/bin/geckodriver"))
driver = webdriver.Firefox(profile, options=options, executable_path=gecko_binary, firefox_binary=firefox_binary)


URL = "http://www.thegreatcourses.com/courses/albert-einstein-physicist-philosopher-humanitarian.html"
#URL = "https://www.thegreatcourses.com/courses/critical-business-skills-for-success"
def getLecturerInfoPhoto(driver, HTML):
    multProfs = "Professor 1 of "
    LecturerDict = {'name' : [], 'role' : [], 'img' : []}
    
    soup = BeautifulSoup(HTML, features="html.parser")
    ProfessorBlock = soup.find('div', {'class' : 'ProductPage-Professor-Info'})
    
    if multProfs in ProfessorBlock.p.getText():
    
        ProfessorBlocks = soup.find_all('div', {'class' : 'ProductPage-Professor-Info'})
        for ProfessorBlock in ProfessorBlocks: 
            LecturerDict['name'].append(ProfessorBlock.h2.getText())
            
            
            roleBlock = ProfessorBlock.find('p', { 'class' : 'ProductPage-Professor-Association' })  
            LecturerDict['role'].append(roleBlock.getText().replace("Institution", ""))
                
        ProfImageBlocks = soup.find_all('div', {'class' : 'ProductPage-Professor-Image'})
        for ProfImageBlock in ProfImageBlocks:
            LecturerDict['img'].append(ProfImageBlock.img['src'])
            
    else:         
        # Name
        LecturerDict['name'].append(ProfessorBlock.h2.getText())
        # Institution (Directory)
        LecturerDict['role'].append(ProfessorBlock.p.getText().replace("Institution", ""))
        # Image Resource
        ProfImageBlock = soup.find('div', {'class' : 'ProductPage-Professor-Image'})
        LecturerDict['img'].append(ProfImageBlock.img['src'])
        
    return LecturerDict


driver.get(URL)
time.sleep(random.randint(13,30))

HTML = driver.page_source

#with open('lecture2.html') as FollowerFile:
#    html = FollowerFile.read()
        
LecturerDict = getLecturerInfoPhoto(driver, HTML)


for k in range(len(LecturerDict['name'])):
    print("--------%s--------" % k) 
    print(LecturerDict['name'][k])
    print(LecturerDict['role'][k])
    print(LecturerDict['img'][k])
    

#for key in LecturerDict.keys():
#    for ele in LecturerDict[key]:
#        print("%s: %s" % (key,ele))


# Get Description
'''
Description = ''
driver.find_element_by_css_selector('.btn-ghost-secondary').click()
time.sleep(random.randint(5,8))
HTML = driver.page_source
soup = BeautifulSoup(HTML, features="html.parser")
DescriptionBlock = soup.find('div', {'class' : 'ProductPage-Overview-Description'})
print(DescriptionBlock.getText())


#html1 = 'lecture1.html'
#with open(html1) as f:
#    HTML = f.read()
    
#soup = BeautifulSoup(HTML, features="html.parser")
#DescriptionBlock = soup.find('div', {'class' : 'ProductPage-Overview-Description'})
pDescBlock = DescriptionBlock.find_all(['p', 'li'])

brre = re.compile("<br")
html_re = re.compile("<.*?>")



wrapper = textwrap.TextWrapper(width=80)
wrapper.initial_indent = "\t -> "
wrapper.subsequent_indent = "\t   "
for p in pDescBlock:
    #print("%s" % str(p), end='\n')
    paragraphs = re.split("<br\/>", str(p))
    li = re.match("<li>(.*?)<\/li>", str(p))
    for para in paragraphs: 
        para = html_re.sub('', para)
        if li is not None:
            
            for meh in wrapper.wrap(html_re.sub('',li.group(0))):
                Description = ''.join([Description, meh,'\n'])
        else:
            Description = '\n'.join([Description, para, '\n'])
            #print('\n %s' % para, end='\n')
        
print(Description)
# End Description
'''

def getLectureTitles(self, driver):
    try: 
        driver.find_element_by_css_selector("button.btn-link-secondary:nth-child(3)").click()
        time.sleep(random.randint(10,15))
        HTML = driver.page_source
        time.sleep(random.randint(10,13))
        soup = BeautifulSoup(HTML, features="html.parser")
        LectureHeaderBlock = soup.find_all('div', {'class' : 'ProductLectureList-Lecture-Header'})
        LectureTitles = []
        k=1
        for block in LectureHeaderBlock:
            LectureTitles.append(block.getText().replace(str(k), ''))
            k += 1
    except:
        LectureTitles = []
        
    return LectureTitles

#def getLectureDescrip(self, driver):

def getLectureDescs(driver):
    driver.find_element_by_css_selector("button.btn-link-secondary:nth-child(3)").click()
    time.sleep(random.randint(5,9))
    LDescBtns = driver.find_elements_by_class_name("AccordionToggle")
    
    LectureDescriptions = []
    k = 0
     
    for button in LDescBtns:
        try: 
            print("Button %s..." % k)
            driver.execute_script("arguments[0].click();", button)
            #button.click()
            time.sleep(random.randint(3,6))
            HTML = driver.page_source
            soup = BeautifulSoup(HTML, features="html.parser")
            LectDescBlock = soup.find_all('div', {'class' : 'ProductLectureList-Lecture-Content'})
            i = 0
            for block in LectDescBlock:
                if i < k:
                    i += 1 
                    continue
                else:
                    LectureDescriptions.append(block.getText())
                    break
            k += 1
        except Exception as e: 
            LectureDescriptions.append(str(e))
            k += 1
            continue
        
        
    
    
    return LectureDescriptions
'''
LectureDescriptions = getLectureDescs(driver)
k = 1
for desc in LectureDescriptions:
    print("%s.) %s" % (k, desc))
    k += 1
'''

def getRating(driver, HTML):
    soup = BeautifulSoup(HTML, features='html.parser')
    ratingBlock = soup.find('div', {'class' : 'bv-percent-recommend-container'})
    rating = ratingBlock.getText().replace('% of reviewers recommend', '')
    return float(rating)        

rating = getRating(driver, HTML)
print("Rating: %s" % float(rating))
display.stop()
'''

'''

#print(ProfessorBlock.getText())
#driver.quit()


'''
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
    
 


session = HTMLSession()
#session.set_header('User-Agent', USER_AGENT)

r = await session.get(URL, headers=headers)

r =  await r.html.render()  # this call executes the js in the page
ProfessorName = r.absolute_links


print(ProfessorName) 

asyncio.run(process_links())
'''