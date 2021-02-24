# coding: utf-8
#
# TGC.bundle v2.0  (h.l. mencken)
# oh fo sho yo
# coded by: bubonic

from HTMLParser import HTMLParser, HTMLParseError
from htmlentitydefs import name2codepoint


import datetime
import ssl
import sys
import os
import re
import time
import random
import textwrap
import urllib3
import shutil
import subprocess
import hashlib
import platform


try:
    import Levenshtein as lev
except:
    Log("Couldn't Import Levenshtein Algorithm... You must be on a bunnk platform")
    Log("SearchCourse() Will not work... ")
    Log("Make sure you follow the proper naming scheme...")
    Log("Skipping...")
    pass 


from io import open
from whichcraft import which

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options
from pyvirtualdisplay import Display
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup


# EDIT THIS TO THE PATH OF THE EXECUTABLE 
FIREFOX = "/usr/local/bin/firefox/firefox"

# You can leave these alone or edit them if you feel like doing so. PATH TO EXECUTABLE
GECKODRIVER = "/usr/local/bin/geckodriver"
CONVERT = "/usr/bin/convert"

# Global Settings    
PLEXROOT = Core.app_support_path
TGC_COURSE_URL = 'http://www.thegreatcourses.com/courses/'
TGC_SEARCH_URL = 'http://www.thegreatcourses.com/search/?q='
TGC_PLUS_COURSE_URL = 'https://www.thegreatcoursesplus.com/'
TGC_PLUS_SEARCH_URL = 'https://www.thegreatcoursesplus.com/search/?q='
TGC_PLUS_ALL_URL = 'https://www.thegreatcoursesplus.com/categories'
TGC_PLUS_URL2 = 'https://www.thegreatcoursesplus.com/'
TGC_PLUS_URL1 = 'https://www.thegreatcoursesplus.com/show/'
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0'
SEARCHURL = "https://www.thegreatcourses.com/search/"
BASEURL = "http://www.thegreatcourses.com"
JAROMIN = .811337

ONE_DAY = datetime.timedelta(days=1)
TODAY = datetime.date.today()
TGCDB = 'https://drive.google.com/uc?export=download&id=0B0iKKQfjnk-ANGc4ZGxNa3pQZWc'
CHUNKSIZE = 8192


# Variables for Poster art and ImageMagick
AgentImageFolder = os.path.join(PLEXROOT, "Plug-ins", "TGC.bundle", "Contents", "Resources")
PosterTemplate = os.path.join(PLEXROOT, "Plug-ins", "TGC.bundle", "Contents", "Resources", "template.png")
CourseArt = os.path.join(PLEXROOT, "Plug-ins", "TGC.bundle", "Contents", "Resources", "courseart")
CArtResized = " "
global FinalPoster
FinalPoster = os.path.join(PLEXROOT, "Plug-ins", "TGC.bundle", "Contents", "Resources", "final-")


# Need for ImageMagick to create proper poster art
IMGcmd = [os.path.abspath(CONVERT), PosterTemplate, CArtResized , '-gravity', 'center', '-composite' , FinalPoster]
RSZcmd = [os.path.abspath(CONVERT), CourseArt, '-resize', '780', CArtResized]

# Firefox and gecko binaries
firefox_binary = FirefoxBinary(os.path.abspath(FIREFOX))
firefox_binary.add_command_line_options('--headless')
gecko_binary = os.path.abspath(GECKODRIVER)

global CURRENTTAB

# Platform
PLATFORM = platform.system()
#CMDFINDER = "where" if platform.system() == "Windows" else "which"
#product_category = {'901' : "Economics & Finance", '902' : 'High School', '904' : 'Fine-Arts', '905' : 'Literature & Language', '907' : 'Philosophy, Intellectual History','909' : 'Religion', '910' : 'Mathematics', '918' : 'History', '926': 'Science', '927': 'Better Living'   }
def is_tool(name):

    return which(name)

def wait_until(timeout, period):
    mustend = time.time() + timeout
    while time.time() < mustend:
        global UPDATEDONE
        if UPDATEDONE:
            UPDATEDONE = False 
            return True
        time.sleep(period)
    return False

def Start():
    global display
    HTTP.CacheTime = CACHE_1DAY
    HTTP.Headers['User-Agent'] = 'Mozilla/5.0 (iPad; CPU OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11B554a Safari/9537.54'
    HTTP.Headers['Accept-Language'] = 'en-us'
    
    if is_tool("convert") is None:
        Log("Please install ImageMagick to continue. This is used for poster art image processing.")
        sys.exit(7)
    else:
        global CONVERT
        CONVERT = is_tool("convert")
        Log("ImageMagick is installed.")
    
    if is_tool("geckodriver") is None:
        if PLATFORM != "Windows":
            Log("Please install geckodriver")
            sys.exit(7)
        else:
            Log("Assuming geckodriver location is: " + str(GECKODRIVER))
            Log("Edit the variable if not correct")
    else:
        global GECKODRIVER
        GECKODRIVER = is_tool("geckodriver")
        Log("Geckodriver is installed.")
    
    
        
    if PLATFORM != "Windows":
        Log("Starting Display...")
        if is_tool("Xvfb") is not None:
            display = Display(visible=0, size=(1366, 768))
            display.start()
        else:
            Log("You need Xvfb installed to continue on Linux")
            sys.exit(7)
    Log("Staring Selenium driver...")
    global driver
    driver = startWebDriver()
    global TABCOUNT
    TABCOUNT = 0
    global UPDATEDONE
    UPDATEDONE = False


def startWebDriver():
    
    options = Options()
    options.headless = True
    profile = webdriver.FirefoxProfile()
    profile.set_preference("javascript.enabled", True)
    profile.set_preference("webdriver.log.file", "/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Plug-ins/TGC.bundle/firefox.log");
    #cap = DesiredCapabilities().FIREFOX
    #cap["marionette"] = False
    #profile.set_preference("general.useragent.override", "Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0")
    #profile.set_preference("headless", True)
    #driver = webdriver.Firefox(profile, capabilities=cap, options=options, executable_path=gecko_binary, firefox_binary=firefox_binary)
    driver = webdriver.Firefox(profile, options=options, executable_path=gecko_binary, firefox_binary=firefox_binary)
    
    return driver
    
    #driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"),   chrome_options=chrome_options) 
    #driver.set_window_size(1120, 550)
    
    

class TGCAgent(Agent.TV_Shows):
    
    name = 'TGC'
    languages = [Locale.Language.English]
    primary_provider = True
    accepts_from = ['com.plexapp.agents.localmedia']
   
    def processPoster(self, coursenum, courseArt):
        # if i can get PIL to import I'll use this. 
        '''
        background = Image.open(PosterTemplate, 'r')
        bg_w, bg_h = background.size
        course = Image.open(CourseArt, 'r')
        course_w, course_h = course.size
        offset_course = ((bg_w - course_w) // 2, (bg_h - course_h) // 2 )
        background.paste(course, offset_course)
        background.save(FinalPoster)
        '''
        try:
            Log("Resizing courseart...")
            CourseArtResized = CourseArt + "-" + coursenum + "-780" + ".jpg"
            rszcmd = [RSZcmd[0], courseArt, '-resize', '780', CourseArtResized]
            subprocess.Popen(rszcmd)
            
            cmd = [IMGcmd[0], IMGcmd[1], CourseArtResized, IMGcmd[3], IMGcmd[4], IMGcmd[5], IMGcmd[6] + str(coursenum) + ".png"]
            
            FinalPosterTemp = os.path.join(PLEXROOT, "Plug-ins", "TGC.bundle", "Contents", "Resources", "final-")
            
            global FinalPoster
            FinalPoster = FinalPosterTemp + str(coursenum) + ".png"
            
            Log("Creating Final Poster...")
            subprocess.Popen(cmd)
            Log(" " + FinalPoster)

        except Exception as e:
            print("OS Command failed: " + str(e))
            
    def getRating(self, HTML):
        try: 
            soup = BeautifulSoup(HTML, features='html.parser')
            ratingBlock = soup.find('div', {'class' : 'bv-percent-recommend-container'})
            rating = ratingBlock.getText().replace('% of reviewers recommend', '')
            return float(rating)        
        except Exception as e:
            Log("Error getting rating: " + str(e))
            return None
    
    def getStarsRating(self, HTML):
        try: 
            soup = BeautifulSoup(HTML, features='html.parser')
            stars = soup.find('div', {'class' : 'Rating'}).getText()
            return float(stars)
        except Exception as e:
            Log("Error getting stars: " + st(e))
            return None
    
    def getCourseNumber(self, HTML):
        
        soup = BeautifulSoup(HTML, features="html.parser")
        
        try :
            return str(soup.find('p', {'class' : 'ProductPage-Header-CourseNumber'}).getText().replace("Course No. ", ''))
        except Exception as e:
            Log("Error Retrieving Course Number: " + str(e))
            return 0
            
    def getDESC(self, driver):
        Description = ''
        
        driver.find_element_by_css_selector('.btn-ghost-secondary').click()
        time.sleep(random.randint(25,35))
        HTML = driver.page_source
        
        Log("Getting Description...")
        time.sleep(random.randint(25,35))    
        soup = BeautifulSoup(HTML, features="html.parser")
        DescriptionBlock = soup.find('div', {'class' : 'ProductPage-Overview-Description'})
        pDescBlock = DescriptionBlock.find_all(['p', 'li'])
        
        brre = re.compile("<br")
        html_re = re.compile("<.*?>")
        
        wrapper = textwrap.TextWrapper(width=80)
        wrapper.initial_indent = "\t • "
        wrapper.subsequent_indent = "\t   "
        Log("Textwrapping...")
        for p in pDescBlock:
            #print("%s" % str(p), end='\n')
            paragraphs = re.split("<br\/>", str(p))
            li = re.match("<li>(.*?)<\/li>", str(p))
            for para in paragraphs: 
                para = html_re.sub('', para)
                if li is not None:
                    #print('\t • %s' %  html_re.sub('',li.group(0)))
                    for meh in wrapper.wrap(html_re.sub('',li.group(0))):
                        #Description = ''.join([Description, meh,'\n'])
                        Description = '\n'.join([Description, meh])
                else:
                    Description = '\n'.join([Description, para, '\n'])
                    #print('\n %s' % para, end='\n')
                
        return Description
        
    def getLectureTitles(self, driver):
        try:
            driver.find_element_by_css_selector("button.btn-link-secondary:nth-child(3)").click()
            time.sleep(random.randint(10,15))
        except:
            Log("10 or less lectures")
            pass
        HTML = driver.page_source
        soup = BeautifulSoup(HTML, features="html.parser")
        LectureHeaderBlock = soup.find_all('div', {'class' : 'ProductLectureList-Lecture-Header'})
        LectureTitles = []
        k=1
        for block in LectureHeaderBlock:
            LectureTitles.append(block.getText().replace(str(k), ''))
            k += 1
        
        return LectureTitles
    
    def getLectureDescs(self, driver):
        try: 
            driver.find_element_by_css_selector("button.btn-link-secondary:nth-child(3)").click()
        except:
            pass
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

    def getLecturerInfoPhoto(self, driver, HTML):
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
  
    def getGenre(self, cnum):
        subjs = []
        
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        requestPlus = urllib2.Request(TGCDB)
        requestPlus.add_header('User-Agent', USER_AGENT)
        try:
            f = urllib2.urlopen(requestPlus, context=ctx)
            dbfile = f.read()
        except urllib2.HTTPError:        
            Log("urllib2 HTTPError")
            pass
        #response = urllib2.urlopen('https://drive.google.com/uc?export=download&id=0B0iKKQfjnk-ANGc4ZGxNa3pQZWc')
        #dbfile = response.read()
        
        for course in dbfile.splitlines():
            courseID = course.split('|',1)[0]
            if cnum == courseID:
                genre = course.split('|',2)[-1]
                subjs.append(genre)

        return subjs
    
    '''
    def searchPlusURL(self, course, courseID):
        fixCourse = course
        sResultsSPAN = [ ]
        sResults = [ ]
        spanLen = [ ]
        plusURL = ''
        course_found = 0
        
        courses = { 'CTITLE': [], 'CLINK': [], 'CID': [], 'TAX1': [], 'TAX2': [] }
        courseRET = { 'URL': None, 'TAX1': None, 'TAX2': None }
        linkre = re.compile("COURSE_LINK.*")
        ctitlere = re.compile("COURSE_TITLE.*")
        cnumre = re.compile("COURSE_ID.*")
        tax1re = re.compile("TAXONOMY1.*")
        tax2re = re.compile("TAXONOMY2.*")
        
        course = course.replace(':', '')
        course = course.replace('"', '')
        course = course.replace(',', '')
        course = course.replace('?', '')
        course = course.replace(' ', '.*')
        course = course.replace('&', '.')
        course = course.replace('The', '.*')
        course = course.replace('the', '.*')
        course = course.replace('of', '.*')

        re_course = re.compile(course, re.DOTALL | re.IGNORECASE)
        
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        requestPlus = urllib2.Request(TGC_PLUS_ALL_URL)
        requestPlus.add_header('User-Agent', USER_AGENT)
        try:
            f = urllib2.urlopen(requestPlus, context=ctx)
            htmlPlus = f.read()
        except urllib2.HTTPError:        
            Log("urllib2 HTTPError")
            pass

        for line in htmlPlus.splitlines():
            linklst = linkre.findall(line)
            ctitlelst = ctitlere.findall(line)
            cidlst = cnumre.findall(line)
            tax1lst = tax1re.findall(line)
            tax2lst = tax2re.findall(line)
            if linklst:
                link = linklst[0]
                link = link.split(':',1)[-1]
                link = link.replace(',', '')
                link = link.replace('"', '')
                if '?' in link:
                    link = link.split('?',1)[0]
                if not linkre.search(link):
                    courses['CLINK'].append(link)
            if ctitlelst:
                ctitle = ctitlelst[0]
                ctitle = ctitle.split(':',1)[-1]
                ctitle = ctitle.replace(',', '')
                ctitle = ctitle.replace('"', '')
                if not ctitlere.search(ctitle):
                    courses['CTITLE'].append(ctitle)
            if cidlst:
                cnum = cidlst[0]
                cnum = cnum.split(':',1)[-1]
                cnum = cnum.replace(',','')
                cnum = cnum.strip()
                if not cnumre.search(cnum):
                    courses['CID'].append(cnum)           
            if tax1lst:
                tax1 = tax1lst[0]
                tax1 = tax1.split(':',1)[-1]
                tax1 = tax1.replace(',','')
                tax1 = tax1.replace('"', '')
                tax1 = tax1.strip()
                if not tax1re.search(tax1):
                    courses['TAX1'].append(tax1)
            if tax2lst:
                tax2 = tax2lst[0]
                tax2 = tax2.split(':',1)[-1]
                tax2 = tax2.replace(',','')
                tax2 = tax2.replace('"', '')
                tax2 = tax2.strip()
                if not tax2re.search(tax2):
                    courses['TAX2'].append(tax2)

        
        i=0
        if courseID != 0:
            for key, value in courses.iteritems():
                if key == 'CID':
                    for CNUM in value:
                        if CNUM == courseID:
                            Log("TGC+ COURSE FOUND!")
                            Log("%s : %s : %s" % (courses['CID'][i], courses['CTITLE'][i], courses['CLINK'][i]))
                            course_found = 1
                            plusURL = ''.join([TGC_PLUS_COURSE_URL, courses['CLINK'][i].strip()])
                            courseRET['URL'] = plusURL
                            courseRET['TAX1'] = courses['TAX1'][i]
                            courseRET['TAX2'] = courses['TAX2'][i]
                            break
                        i = i + 1 
        else:                
            for key, value in courses.iteritems():
                if key == 'CTITLE':
                    for xtitle in value:
                        re_course_match = re_course.search(xtitle)
                        if re_course_match is not None:
                            Log("TGC PLUS MATCH FOUND!") 
                            sResults.append(i)
                            sResultsSPAN.append(re_course_match.span())
             
                        i = i + 1
            for spanR in sResultsSPAN:
                spanLen.append(spanR[1] - spanR[0])
            

            try:
                cindex = spanLen.index(max(spanLen))
                matchindex = sResults[cindex]
                Log("TGC+ match found for: %s" % fixCourse)
                Log("%s : %s" % (courses['CTITLE'][matchindex], courses['CLINK'][matchindex]))        
                plusURL = ''.join([TGC_PLUS_COURSE_URL, courses['CLINK'][matchindex].strip()])
                courseRET['URL'] = plusURL
                courseRET['TAX1'] = courses['TAX1'][matchindex]
                courseRET['TAX2'] = courses['TAX2'][matchindex]
                Log("%s" % plusURL)
                course_found = 1
            except ValueError:
                Log("No indexes to find b/c no matches in TGC+ courses")
                plusURL = None
                
        if course_found == 1:   
            return courseRET
        else:
            Log("NO TGC+ COURSE FOUND.")
            return None 

       
    def getLectureThumbs(self, url):
        lectureThumbs = []
        i=1
    
        Log("Finding lecture thumbs URL: %s" % url)
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        requestPlus = urllib2.Request(url)
        requestPlus.add_header('User-Agent', USER_AGENT)
        try:
            f = urllib2.urlopen(requestPlus, context=ctx)
            htmlPlus = f.read()
        except urllib2.HTTPError:        
            Log("urllib2 HTTPError")
            pass

        soup = BeautifulSoup(htmlPlus)
        lectureThumbBlock = soup.findAll('div', { 'class' : 'list-tray-item-image-container'} )
        for lThumb in lectureThumbBlock:
            link = lThumb.img
            try: 
                thumbImg = link['src']
            except KeyError:
                thumbImg = link['data-src']
            Log("Lecture %s thumbURL: %s" % (i, thumbImg))
            i += 1
            lectureThumbs.append(thumbImg)
       
        if lectureThumbs:
            Log("Found Lecture Thumbs! Quitting getLectureThumbs()")
        else:
            Log("No Lecture thumbs found at url: %s" % url)
                
        return lectureThumbs
    '''  
    
    def scrollWindow(self, driver, scroll):
        a = 1.7
        b = 4.7
        i = 0
        courseURLs = []
        courseTitles = []
        courseDict = { }
        # Get scroll height
        #last_height = driver.execute_script("return document.body.scrollHeight")
        scrollCount = 0
        while True:
            # Scroll down to bottom
            #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            driver.execute_script("window.scrollBy(0,314);")
    
            # Wait to load page
            time.sleep(random.randint(a*10,b*10)/10)
    
            HTML = driver.page_source
            
            soup = BeautifulSoup(HTML, features="html.parser")
            postsBlock = soup.find_all('a', {'class': 'CourseTile-TitleLink'})
            for spblock in postsBlock:
                courseURLs.insert(i, spblock['href'])
                courseTitles.insert(i, spblock.getText())
                courseDict[spblock.getText()] = spblock['href']
                #print(postURLs[i])
                i += 1        
            # Calculate new scroll height and compare with last scroll height
            scrollCount += 1
            if scrollCount > int(scroll):
                break
            
        courseURLs = list(dict.fromkeys(courseURLs))
        courseTitles = list(dict.fromkeys(courseTitles))
        return courseDict

    def SearchCourse(self, title, driver):
        reCourse = re.search('TGC[0-9]{1,4}', title, re.IGNORECASE)
        if reCourse is not None:
            rg = re.compile("TGC", re.IGNORECASE)
            courseno = rg.split(title)[-1].replace(')', '')

            rawTitle = rg.split(title)[0]
            rawTitle = rawTitle.replace('(', '')
            rawTitle = rawTitle.replace(')', '')
            Log("Raw Tit: " + rawTitle)
        else:
            rawTitle = title
            Log("Raw Tit: " + rawTitle)
        
        reTitle = re.search('TTC -', rawTitle, re.IGNORECASE)
        
        if reTitle is not None:
            retit = re.compile('TTC -', re.IGNORECASE)
            bareTit = retit.split(rawTitle)[-1].lstrip()
        else:
            bareTit = rawTitle
            
        bareTit = re.sub(r'\([^)]*\)', '',bareTit)
        bareTit = re.sub(r'\[[^)]*\]', '',bareTit)
        bareTit = re.sub(r'\([^)]*', '',bareTit)
    
        bareTit = bareTit.replace("--", "-")
        bareTit = bareTit.replace("_", ",")
        bareTits = bareTit.split("-")
        
        urlTit = bareTit.replace(' ', '%20')
        urlTit = SEARCHURL + urlTit
            
        Log("BareTit: " + bareTit)
        Log("Search URL: " + urlTit)
        
        Log("Searching for course...")
        driver.get(urlTit)
        time.sleep(random.randint(7,14))
        courseDict = self.scrollWindow(driver, 5)
        k = 0
        jaroDict = {}
        for key, url in courseDict.items():
            jaro_value1 = lev.jaro(bareTits[0].encode('utf-8').lstrip(), key.encode('utf-8'))
            try :
                jaro_value2 = lev.jaro(bareTits[1].encode('utf-8').lstrip(), key.encode('utf-8'))
            except:
                jaro_value2 = 0.0
            jaro_value3 = lev.jaro(bareTit.encode('utf-8').lstrip(), key.encode('utf-8'))
            jaro_max_value = max(jaro_value1, jaro_value2, jaro_value3)
            jaroDict[key] = jaro_max_value
            Log("Title: " + key + ", URL: " + url)
            Log("Jaro Value: " + str(jaroDict[key]))
    
            k += 1
        
        # find max jaro value
        maxjaro = max(jaroDict.values())
        res = [(k, v) for k, v in jaroDict.items() if v == maxjaro]
        Log("------------------Result--------------------")
        result_tuple = res[0]
        keyresult = result_tuple[0]
        result_url = courseDict[keyresult]
        acceptableAnswerURL = BASEURL + result_url
        if maxjaro > JAROMIN: 
            Log("MATCH FOUND!")
            Log("Title: " + keyresult + ", URL: " + BASEURL + result_url + ", Jaro: " + str(maxjaro))
            Results = {'title' : keyresult, 'url' : acceptableAnswerURL, 'jaro' : maxjaro}
        else:
            Log("No signifcant match found, skipping...")
            Results = None
            #print("MaxJaro was: %s" % maxjaro)
            #print("Title: %s \nURL: %s \nJaro: %s" % (keyresult, BASEURL + result_url, maxjaro))
        
        return Results    
    
    
    def search(self, results, media, lang, manual=False):
        id2 = media.show
        id2 = id2.replace("'", ' ')
        id2 = id2.replace('"', ' quot ')
        show = media.show.lower()
        show = show.replace(' ', '-')
        show = show.replace(':', '')
        show = show.replace(',', '')
        show = show.replace(' "', ' quot ')
        show = show.replace('" ', ' quot ')
        show = show.replace('?', '')
        show = show.replace("'", "-")
        Log("show value: %s" % show)
        courseURL = ''.join([TGC_COURSE_URL, show, '.html'])
        Log("Did the search")
        Log("CourseURL %s" % courseURL)  
        Log("Media name: %s" % media.name)  
        results.Append(
             MetadataSearchResult(
                id = id2,
                name = id2,
                year = 2017,
                score = 99,
                lang = lang
            )
        )
        Log("Added results")
    
            

    def update(self, metadata, media, lang):

        Log("def update()")
        global TABCOUNT
        global UPDATEDONE
        TABCOUNT += 1
        Log("TAB: " + str(TABCOUNT))
        show = metadata.id
        mdatashow = show.replace('quot', '"')
        mdatashow = mdatashow.replace(' s ', "'s ")
        reCourse = re.search('TGC[0-9]{1,4}', mdatashow, re.IGNORECASE)
        if reCourse is not None:
            rg = re.compile("TGC", re.IGNORECASE)
            cNum = rg.split(mdatashow)[-1]
            #cNum = mdatashow.split('[',1)[-1]
            #cNum = cNum.replace(']','')
            #cNum = cNum.split('TGC',1)[-1]
            Log("Course Number: %s"  % cNum)
            searchableTit = rg.split(mdatashow)[0]
        else:
            searchableTit = mdatashow
            cNum = 0
        #metadata.title = mdatashow
        
        show = searchableTit
        show = show.lower()
        show = show.replace(':', '')
        show = show.replace(',', '')
        show = show.replace('"', ' quot ')
        #show = show.replace('" ', ' quot ')
        show = show.replace('?', '-')
        show = show.replace("'", "-")
        show = show.replace('–', ' ')
        show = show.replace('  ', ' ')
        show = show.replace(' ', '-')
        courseURL = ''.join([TGC_COURSE_URL, show, '.html'])
        courseURL = courseURL.replace('-.html', '.html')
        
        Log("update() CourseURL: %s" % courseURL)
        

        
        try: 
            Log("Opening tab...")
            if TABCOUNT > 1: 
                Log("Multiple tabs open... Waiting...")
                if wait_until(TABCOUNT*600, .25):
                    Log("Opening subsequent tab...")
                    driver.get(courseURL)
                    global CURRENTTAB
                    CURRENTTAB = driver.current_window_handle
                else:
                    Log("A previous update() took too long. Let's aim for the stars and try it anyway...")
                    #driver.execute_script("window.open(''), '_blank'")
                    driver.execute_script("window.open('"+courseURL+"', '__blank__');")
                    global CURRENTTAB
                    CURRENTTAB = driver.current_window_handle
                    #driver.switch_to_window(driver.window_handles[TABCOUNT - 1])
                    #driver.get(courseURL)
            else:
                driver.get(courseURL)
                global CURRENTTAB
                CURRENTTAB = driver.current_window_handle
            
            
            # check for 404 error, if + then do a search for course
            time.sleep(random.randint(12,17))
            HTML = driver.page_source
            
            # Course Title
            soup = BeautifulSoup(HTML, features="html.parser")
            titleBlock = soup.find('div', {'class' : 'ProductPage-Header-Title'})
            metadata.title = titleBlock.h1.getText() 
            Log("metadata.title: " + metadata.title)
        except Exception as e:
            Log("Error fetching course URL: " + str(e))
            Log("Searching...")
            Result = self.SearchCourse(searchableTit, driver)
            if Result is None:
                Log("Nada, skipping...")
                TABCOUNT = TABCOUNT - 1
                Log("Reducing TABCOUNT: " + str(TABCOUNT))
                if len(driver.window_handles) > 1:
                    driver.close()
                UPDATEDONE = True
                return 
            else: 
                courseURL = Result['url']
                try: 
                    driver.get(courseURL)
                    time.sleep(random.randint(12,17))
                    HTML = driver.page_source
                    
                    # Course Title
                    soup = BeautifulSoup(HTML, features="html.parser")
                    titleBlock = soup.find('div', {'class' : 'ProductPage-Header-Title'})
                    metadata.title = titleBlock.h1.getText() 
                    Log("metadata.title: " + metadata.title)
                except:
                    Log("IM having issues. Forgetting this one.")
                    return
            
 
        metadata.studio = "TGC"
        
        Log("Course Number from local metadata: " + str(cNum))
        Log("Finding course number on courseURL...")
        coursenum= self.getCourseNumber(HTML)
        Log("Course Number: " + coursenum)
        
        if int(cNum) != int(coursenum) and int(coursenum) > 0:
            cNum = coursenum
    
        
        try:
            CourseDesc = self.getDESC(driver)
            Log("Adding metadata summary...")
            Log("Course Description: " + CourseDesc)
            metadata.summary = CourseDesc
        except Exception as e:
            Log("Could not get Course Summary: " + str(e))
            pass
        
        
        try:
            Log("Getting Lecture Titles...")
            LectureTitles = self.getLectureTitles(driver)
        except Exception as e:
            Log("Could not get Lecture titles: " + str(e))
            pass
        
    
        try:
            Log("Getting Lecture Descriptions...")
            LectureDescriptions = self.getLectureDescs(driver) 
        except Exception as e:
            Log("Could not get Lecture Descriptions: " + str(e))
            pass
        
        try: 
            Log("Getting Lecturer(s) Info(s) and Photo(s)...")
            LecturerDict = self.getLecturerInfoPhoto(driver, HTML)
        except Exception as e:
            Log("Error getting lecturer infos: " + str(e))
        
        Log("Populating actors and images...")
        # populate the 'actors'
        try: 
            meta_people_obj = metadata.roles
            for k in range(len(LecturerDict['name'])):
                meta_people_obj.clear()
                meta_role = meta_people_obj.new()
                meta_role.name = LecturerDict['name'][k]
                meta_role.role = LecturerDict['role'][k]
                meta_role.photo = LecturerDict['img'][k]
        except Exception as e:
            Log("Could not set actor/director info: " + str(e))
            
        try: 
            Log("Getting Rating...")
            rating = self.getRating(HTML)
            Log("Rating is: " + str(rating))
            metadata.rating = float(rating / 10)
            Log("Metadata.rating: " + str(metadata.rating))
        except Exception as e:
            Log("Error getting and setting rating: " + str(e))
        
        
        Log("Getting Stars...")
        stars = self.getStarsRating(HTML)
        Log("Stars is: " + str(stars))
        try:
            metadata.user_rating = stars
            Log("Metadata.stars: " + str(metadata.stars))
        except:
            try:
                metadata.star_rating = stars
                Log("Metadata.stars: " + str(metadata.star_rating))
            except:
                try: 
                    metadata.rating_user = stars 
                    Log("Metadata.stars: " + str(metadata.rating_user))
                except:
                    try: 
                        metadata.rating_star = stars
                        Log("Metadata.stars: " + str(metadata.rating_star))
                    except:
                        Log("all stars failed... Skipping...")
                        try:
                            metadata.rating.user = getStarsRating
                        except:
                            pass
                        pass
                    pass
                pass
            pass
        
                    
        
        # Fix searchCourse()
            
        # this just keeps it simple so there is less code rewriting in 
        # updating the episode (lecture) infos
        if LectureTitles is not None and LectureDescriptions is not None:
            eSummaryData = LectureDescriptions
            eTitleData = LectureTitles
        else:
            Log("No lecture title or description info")
        
        
        # Add TGC+ Search for genre and other infos
        coursePlusInfo = None
        
        #Log("Visiting TGC+ companion website if it exists...")
        #coursePlusInfo = self.searchPlusURL(metadata.title, cNum)
        '''
        if coursePlusInfo is not None:
            metadata.genres = [coursePlusInfo['TAX1'], coursePlusInfo['TAX2']]
            lThumbs = self.getLectureThumbs(coursePlusInfo['URL'])
        else:
            Log("No TGC+ companion site to retrieve lecture thumbs.")
            lThumbs = None
        
        if cNum != 0:
            Log('Getting genre...')
            subjs = self.getGenre(cNum)
            Log('Genres: %s' % subjs)
            metadata.genres = subjs
        else:
            Log('No Course ID, so no genres!')
                
        '''
        
        
        
        Log("Updating episode data")
        @parallelize
        def UpdateEpisodes(html=HTML, eSummaryData=eSummaryData, eTitleData=eTitleData):
            Log("def UpdateEpisodes()")
            if media is not None:
                Log("Media is not None")
                for season_num in media.seasons:
                    Log("Season Number:%s" % season_num)
                    episodes = media.seasons[str(season_num)].episodes
                    Log("Episodes: %s" % episodes)
                    for episode_num in media.seasons[str(season_num)].episodes:
                        Log("Episode number:%s" % episode_num)
                        if int(episode_num) != 0:
                            episode = metadata.seasons[str(season_num)].episodes[str(episode_num)]
                            Log("Running UpdateEpisode...")
                            @task
                            def UpdateEpisode(episode=episode, html=html, episode_num=episode_num, eSummaryData=eSummaryData, eTitleData=eTitleData):
                                Log("def UpdateEpisode()")
                                lecture_len = len(eSummaryData)
                                Log("Lecture array length: %s" % lecture_len)
                                if int(episode_num) <= lecture_len:
                                    Log("Episode Title: %s" % eTitleData[int(episode_num) - 1])
                                    Log("Episode summary %s" % eSummaryData[int(episode_num) - 1].strip())
                                    episode.title = str(eTitleData[int(episode_num) - 1 ])
                                    episode.summary = str(eSummaryData[int(episode_num) - 1].strip())
                                    if episode.rating is None:
                                        episode.rating = float(rating / 10)
                                    Log("episode.summary: %s" % episode.summary)
                                    Log("episode.title: %s" % episode.title)
                                    '''
                                    Log("Getting lecture thumb image")
                                    if not lThumbs:
                                        Log("No Episode thumbs avaialbe")
                                    else:
                                        Log("Episode thumbs are avaialbe!")
                                        if lThumbs[int(episode_num) - 1] not in episode.thumbs:
                                            try:
                                                episode.thumbs[lThumbs[int(episode_num) - 1 ]] = Proxy.Preview(HTTP.Request(lThumbs[int(episode_num) - 1]).content, sort_order=1)
                                            except: 
                                                Log("Download of thumb image failed! - %s" % lThumbs[int(episode_num)])
                                                pass
                                    '''    
                                    #Log("Getting Lecturer")
                                
                                '''
                                Log("Lecturer: %s" % lecturer)
                                #episode.directors.clear()
                                #episode.writers.clear()
                                #episode.directors.add(lecturer)
                                #episode.writers.add(lecturer)
                                #Thanks to ZeroQI for the directors edit
                                episode.directors.clear()
                                meta_director = episode.directors.new()
                                #COUNT=0
                                if lecturer == "many": 
                                    for pname in pNames:
                                        meta_director = episode.directors.new()
                                        meta_director.name = pname 
                                        #meta_director.role = pname
                                        #COUNT = COUNT + 1
                                else:
                                    meta_director.name = pName # role name
                                    meta_director.role = lrole # actor name
                                #meta_role.photo = None #url of actor photo
                                if pURL is not None:
                                    meta_director.photo = pURL #url of actor photo
                                    Log("meta_director.photo: %s" % meta_director.photo)
                                #Log("episode.directors: %s" % episode.directors)
                                #Log("episode.writers: %s" % episode.writers)
                                '''
                                Log("Setting episode dates")    
                                if episode_num == 1:
                                    episode.originally_available_at = TODAY
                                    Log("For episode: %s the date is %s" % (episode_num, episode.originally_available_at))
                                else:
                                    tdelta = datetime.timedelta(days=int(episode_num))
                                    newDate = TODAY + tdelta
                                    episode.originally_available_at = newDate
                                    Log("For episode: %s the date is %s" % (episode_num, episode.originally_available_at))
                        else:
                            Log("I do not update episodes 0. No Information to retrieve.")    
                    
                    
        #episode.rating = rating
        
        Log("Downloading Art...")
        @parallelize
        def DownloadArt(coursenum=cNum):
            valid_posters = []
            valid_art = []
            arturl = "https://secureimages.teach12.com/tgc/images/m2/courses/high/" + str(coursenum) + ".jpg"
            @task
            def DownloadPoster(poster_url=arturl, filePath=FinalPoster):
                Log("Downloading poster...")
                try:
                    c = urllib3.PoolManager()
                    #metadata.posters[poster_url] = Proxy.Preview(HTTP.Request(poster_url).content, sort_order=1)
                    courseArt = CourseArt + "-" + coursenum + ".jpg"
                    with c.request('GET', poster_url, preload_content=False) as res, open(courseArt, 'wb') as out_file:
                        shutil.copyfileobj(res, out_file)
                    self.processPoster(coursenum, courseArt)
                    
                    # Load the file
                    time.sleep(random.randint(7,14))
                    data = Core.storage.load(FinalPoster)
                    poster_name = hashlib.md5(data).hexdigest()
                    valid_posters.append(poster_name)
                    if poster_name not in metadata.posters:
                        metadata.posters[poster_name] = Proxy.Media(data)
                        
			        #Log("Proxy.Media(data) - FIGURE THIS OUT")
                    #metadata.posters[poster_url] = Proxy.Preview(HTTP.Request(FinalPoster).content, sort_order=1)
                    data = Core.storage.load(courseArt)
                    art_name = hashlib.md5(data).hexdigest()
                    valid_art.append(art_name)
                    if art_name not in metadata.art:
                        metadata.art[art_name] = Proxy.Media(data)
                except Exception as e:
                    Log("Download of poster image failed! - %s" % arturl)
                    Log("ERROR: " + str(e))
                    pass
            metadata.posters.validate_keys(valid_posters)
            metadata.art.validate_keys(valid_art)
 
            
        Log("Cleaning up...")
        #if TABCOUNT > 1:
        #    time.sleep(random.randint(15,60))
        #    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')
        #display.stop()
        #self.Stop()
        Log("Done")
        UPDATEDONE = True
        Log("Driver Handles: "  + str(len(driver.window_handles)))
        if len(driver.window_handles) > 1:
            driver.close()
        TABCOUNT = TABCOUNT - 1
        #return
