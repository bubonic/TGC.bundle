# coding: utf-8
from HTMLParser import HTMLParser, HTMLParseError
from htmlentitydefs import name2codepoint
from BeautifulSoup import BeautifulSoup 
import datetime
import ssl
import sys
import os
import re


try:
    # For Python 3.0 and later
    from urllib.request import urlopen
    import urllib
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen
    import urllib2
    

TGC_COURSE_URL = 'http://www.thegreatcourses.com/courses/'
TGC_SEARCH_URL = 'http://www.thegreatcourses.com/search/?q='
TGC_PLUS_COURSE_URL = 'https://www.thegreatcoursesplus.com/'
TGC_PLUS_SEARCH_URL = 'https://www.thegreatcoursesplus.com/search/?q='
TGC_PLUS_ALL_URL = 'https://www.thegreatcoursesplus.com/categories'
TGC_PLUS_URL2 = 'https://www.thegreatcoursesplus.com/'
TGC_PLUS_URL1 = 'https://www.thegreatcoursesplus.com/show/'
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0'
ONE_DAY = datetime.timedelta(days=1)
TODAY = datetime.date.today()
TGCDB = 'https://drive.google.com/uc?export=download&id=0B0iKKQfjnk-ANGc4ZGxNa3pQZWc'
#product_category = {'901' : "Economics & Finance", '902' : 'High School', '904' : 'Fine-Arts', '905' : 'Literature & Language', '907' : 'Philosophy, Intellectual History','909' : 'Religion', '910' : 'Mathematics', '918' : 'History', '926': 'Science', '927': 'Better Living'   }

# For Sure yo, coded by bubonic

def Start():

    HTTP.CacheTime = CACHE_1DAY
    HTTP.Headers['User-Agent'] = 'Mozilla/5.0 (iPad; CPU OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11B554a Safari/9537.54'
    HTTP.Headers['Accept-Language'] = 'en-us'
    
class TGCAgent(Agent.TV_Shows):
    
    name = 'TGC'
    languages = [Locale.Language.English]
    primary_provider = True
    accepts_from = ['com.plexapp.agents.localmedia']

    class MyDESCParser(HTMLParser):
        def __init__(self):
            HTMLParser.__init__(self)
            self.recording = 0
            self.data = []

        def handle_starttag(self, tag, attributes):
            if tag != 'div':
                return
            if self.recording:
                self.recording = self.recording + 1
                return
            for name, value in attributes:
                if name == 'class' and value == 'course-description':
                    break
            else:
                return
            self.recording = 1

        def handle_endtag(self, tag):
            if tag == 'div' and self.recording:
                self.recording = self.recording - 1

        def handle_data(self, data):
            if self.recording:
                self.data.append(data)
    
    class MyLTITLEParser(HTMLParser):
        def __init__(self):
            HTMLParser.__init__(self)
            self.recording = 0
            self.data = []
            self.newdata = 0
            self.c = ''
            self.c2 = ''
            self.newdata2 = []
            self.switch = 0

        def handle_starttag(self, tag, attributes):
            if tag != 'div':
                return
            if self.recording:
                self.recording = self.recording + 1
                return
            for name, value in attributes:
                if name == 'class' and value == 'lecture-title':
                    self.switch = 0
                    break
            else:
                return
            self.recording = 1

        def handle_endtag(self, tag):
            if tag == 'div' and self.recording:
                self.recording = self.recording - 1

        def handle_data(self, data):
            if self.recording:
                if data and data != 'x':
                    if self.switch == 1:
                        last = self.data.pop()
                        self.newdata = ' '. join([last, data])
                        self.data.append(self.newdata)
                        self.switch = 0
                    else:
                        self.data.append(data)

        def handle_entityref(self, ref):
            # called for each entity reference, e.g. for "&copy;", ref will be "copy"
            if ref in ('lt', 'gt', 'quot', 'amp', 'apos'):
                text = '&%s;' % ref
            else:
                # entity resolution graciously donated by Aaron Swartz
                def name2cp(k):
                    import htmlentitydefs
                    k = htmlentitydefs.entitydefs[k]
                    if k.startswith("&#") and k.endswith(";"):
                        return int(k[2:-1]) # not in latin-1
                    return ord(k)
                try: name2cp(ref)
                except KeyError: text = "&%s;" % ref
                else: text = unichr(name2cp(ref)).encode('utf-8')
            self.c = text
            if self.data and self.recording:
                last = self.data.pop()
                self.newdata = ''.join([last,self.c])
                self.data.append(self.newdata)
                #print "Newdata:     ", self.newdata
                self.switch = 1

        def handle_charref(self, name):
            if name.startswith('x'):
                self.c2 = chr(int(name[1:], 16))
            else:
                try:
                    self.c2 = chr(int(name))
                except (TypeError, ValueError):
                    Log("unknown character")

            if self.data and self.recording:
                last = self.data.pop()
                self.newdata2 = ''.join([last,self.c2])
                self.data.append(self.newdata2)
                self.switch = 1

    class MyLDESCParser(HTMLParser):
        def __init__(self):
            HTMLParser.__init__(self)
            self.recording = 0
            self.data = []
            self.newdata = 0
            self.newdata2 = 0
            self.c = ''
            self.c2 = ''
            self.switch = 0

        def handle_starttag(self, tag, attributes):
            if tag == 'em' and self.recording:
                self.switch = 1
            if tag != 'div':
                return
            if self.recording:
                self.recording = self.recording + 1
                return
            for name, value in attributes:
                if name == 'class' and value == 'lecture-description-block left' or value == 'lecture-description-block right':
                    break
            else:
                return
            self.recording = 1

        def handle_endtag(self, tag):
            if tag == 'a' and self.recording:
                self.recording = self.recording - 1
            elif tag == 'em' and self.recording:
                self.switch = 1

        def handle_data(self, data):
            if self.recording:
                if data and data != 'x' and data != ' ':
                    if self.switch == 1:
                        last = self.data.pop()
                        self.newdata = ''. join([last, data])
                        self.data.append(self.newdata)
                        self.switch = 0
                    else:
                        data.strip()
                        self.data.append(data)


        def handle_entityref(self, ref):
            # called for each entity reference, e.g. for "&copy;", ref will be "copy"
            if ref in ('lt', 'gt', 'quot', 'amp', 'apos'):
                text = '&%s;' % ref
            else:
                # entity resolution graciously donated by Aaron Swartz
                def name2cp(k):
                    import htmlentitydefs
                    k = htmlentitydefs.entitydefs[k]
                    if k.startswith("&#") and k.endswith(";"):
                        return int(k[2:-1]) # not in latin-1
                    return ord(k)
                try: name2cp(ref)
                except KeyError: text = "&%s;" % ref
                else: text = unichr(name2cp(ref)).encode('utf-8')
            self.c = text
            if self.data and self.recording:
                last = self.data.pop()
                self.newdata = ''.join([last,self.c])
                self.data.append(self.newdata)
                #print "Newdata:     ", self.newdata
                self.switch = 1


        def handle_charref(self, name):
            if name.startswith('x'):
                self.c2 = chr(int(name[1:], 16))
            else:
                try:
                    self.c2 = chr(int(name))
                except (TypeError, ValueError):
                    Log("unknown character")    
            if self.data and self.recording:
                last = self.data.pop()
                self.newdata2 = ''.join([last,self.c2])
                self.data.append(self.newdata2)
                self.switch = 1

    class MyLecturerParser(HTMLParser):
        def __init__(self):
            HTMLParser.__init__(self)
            self.recording = 0
            self.data = []

        def handle_starttag(self, tag, attributes):
            if tag != 'span':
                return
            if self.recording:
                self.recording = self.recording + 1
                return
            for name, value in attributes:
                if name == 'class' and value == 'name':
                    break
            else:
                return
            self.recording = 1

        def handle_endtag(self, tag):
            if tag == 'span' and self.recording:
                self.recording = self.recording - 1

        def handle_data(self, data):
            if self.recording:
                self.data.append(data.strip())
    
    def getRating(self, html):
        soup = BeautifulSoup(html)
        ratingBlock = soup.find('span', {'class' : 'BVRRNumber BVRRRatingNumber'})
        rating = ratingBlock.getText()
        rating = 2*float(rating)
        return rating
        
    def getDESC(self, html):
        DESC = ''
        
        parser = self.MyDESCParser()
        parser.feed(html)
        data = parser.data
        
        for desc in data:
            if desc == "Hide Full Description":
                break
            elif desc == "Please Verify Account to Continue":
                break
            if desc.isspace():
                DESC = "\n".join([DESC,desc])
            else:
                DESC = ''.join([DESC,desc])
        
        return DESC.strip()
    
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

    
          
    def SearchCourse(self, mdatashow, cNum):
        course = mdatashow
        fixCourse = course
        CN = 31337

        sResults = { }
        sResultsSPAN = [ ]
        spanLen = [ ]
        sTitleResults = [ ]
        
        
        mdatashow = mdatashow.replace(':', '%3A')
        mdatashow = mdatashow.replace('?', '%3F')
        mdatashow = mdatashow.replace(',', '%2C')
        mdatashow = mdatashow.replace(' ', '+')
        
        course = course.replace(':', '')
        course = course.replace("'s", '')
        course = course.replace('"', '')
        course = course.replace(',', '')
        course = course.replace('?', '')
        course = course.replace('-', '')
        course = course.replace('&', '.*')
        course = course.replace('–', '' )
        course = course.replace(' ', '.*')
        course = course.replace('The', '.*')
        course = course.replace ('the', '.*')
        course = course.replace ('of', '.*')
        course = ''.join(['.*', course])

        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
    
        
        searchURL = ''.join([TGC_SEARCH_URL,mdatashow])
        request = urllib2.Request(searchURL)
        request.add_header('User-Agent', USER_AGENT)
        try:
            f = urllib2.urlopen(request, context=ctx)
            html = f.read()
        except urllib2.HTTPError:        
            Log("urllib2 HTTPError")
            pass

#        opener = urllib2.build_opener()
#        html = opener.open(request, context=ctx).read()
        
        re_course = re.compile(course, re.DOTALL | re.IGNORECASE)
        re_courseSet = re.compile("\(Set\)")
        
        soup = BeautifulSoup(html)
        sresult = soup.findAll(attrs={"class": "item-inner"})
        Log("Locating search results...")
        
        for link in sresult:
            title = link.a['title']
            Log("Title: %s" % link.a['title'])
            re_course_match = re_course.match(title)
            re_set_search = re_courseSet.search(title)
            if re_course_match is not None and re_set_search is None:
                Log("Match found for: %s" % fixCourse)
                Log("Title found is: %s" % title)
                Log("Link is: %s" % link.a['href'])
                sResults.update({title: link.a['href']})
                sResultsSPAN.append(re_course_match.span())
                sTitleResults.append(title)
        
        Log("Finding best match...")
        for spanR in sResultsSPAN:
            spanLen.append(spanR[1] - spanR[0])
            Log("Span length for is: %s" % spanLen[-1])
            
        cindex = spanLen.index(max(spanLen))
        Results = {'title': sTitleResults[cindex], 'href': sResults[sTitleResults[cindex]]}
        #cindex = max(xrange(len(spanLen)), key=spanLen.__getitem__)
        #checking if there is a course number
        if cNum != 0:
            while (CN != cNum):

                Log("CourseTitle is: %s" % sTitleResults[cindex])
                Log("CourseURL is: %s" % sResults[sTitleResults[cindex]])

                resultsURL = sResults[sTitleResults[cindex]]
                request = urllib2.Request(resultsURL)
                request.add_header('User-Agent', USER_AGENT)
                try:
                    f = urllib2.urlopen(request, context=ctx)
                    html = f.read()
                except urllib2.HTTPError:        
                    Log("urllib2 HTTPError")
                    pass    
#                opener = urllib2.build_opener()
#                html = opener.open(request).read()
                soup = BeautifulSoup(html)
  
                #courseNum = soup.find("div", { "class" : "course-number" } )
                #CN = courseNum.getText().split(';',1)[-1]
                courseNum = soup.find("div", { "class" : "course-number" } )
                if courseNum is not None:
                    CN = courseNum.getText().split(';',1)[-1]
                else:
                    courseNum = soup.find("span", { "class" : "course-num" } )
                    CN = courseNum.getText().split('No.', 1)[-1]
                    CN = CN.split(';', 1)[-1].strip()
                Log("Course Number Search: %s" % cNum)
                Log("Course Number Found: %s" % CN)

                if cNum == CN:
                    Results = {'title': sTitleResults[cindex], 'href': sResults[sTitleResults[cindex]]}
                else:
                    del spanLen[cindex]
                    cindex = spanLen.index(max(spanLen))

                    
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
        lecturers = []
        pNames = []
        pNamesURL = []
        lRoles = []

        Log("def update()")
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
            metadata.title = rg.split(mdatashow)[0]
        else:
            metadata.title = mdatashow
            cNum = 0
        #metadata.title = mdatashow
        Log("metadata.title: %s" % metadata.title)
        show = metadata.title
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
        #coursePlusURL = ''.join([TGC_PLUS_COURSE_URL, show])
        #coursePlusURL = coursePlusURL[:-1]
        Log("update() CourseURL: %s" % courseURL)
        #Log("update() CoursePlusURL: %s" % coursePlusURL)

        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
         
        Log("calling urllib2 and visiting coursURL")
        request = urllib2.Request(courseURL)
        request.add_header('User-Agent', USER_AGENT)
#        opener = urllib2.build_opener()
        
        try:
#            html = opener.open(request).read()
            f = urllib2.urlopen(request, context=ctx)
            html = f.read() 
        except urllib2.HTTPError:
            Log("courseURL not found... Searching for related courses: %s" % metadata.title)
            Results = self.SearchCourse(metadata.title, cNum)
            Log("Course found, URL: %s" % Results['href'])
            scourseURL = Results['href']
            metadata.title = Results['title']
            request = urllib2.Request(scourseURL)
            request.add_header('User-Agent', USER_AGENT)
            f = urllib2.urlopen(request, context=ctx)
            html = f.read()
 
#            opener = urllib2.build_opener()
#            html = opener.open(request).read()
            

        data = self.getDESC(html)
        Log("Adding metadata summary")
        metadata.summary = data
        
        Log("Calling MyLDESCParser()")
        parser = self.MyLDESCParser()
        Log("Calling MyLTITLEarser()")
        parser2 = self.MyLTITLEParser()
        Log("Calling MyLDESCParser().feed(html)")
        parser.feed(html)
        Log("Calling MyLTITLEarser().feed(html)")
        parser2.feed((html))
        '''
        Log("Finding lecturers and lecturer photos...")
        proDict = self.getLecturer(html, metadata.roles)
        if proDict['Num'] == "1":
            pName = proDict['Lecturer']
            lrole = proDict['Role']
            pURL = proDict['Photo']
            lecturer = pName
        else:
            lecturer = "many"
            pNames = proDict['Lecturer']
            pURL = None
        '''         
        lecturer="none"
        Log("Getting Rating...")
        rating = self.getRating(html)
        metadata.rating = float(rating)    
        
        metadata.studio = "TGC"
        
        eSummaryData = parser.data
        eTitleData = parser2.data
        
        #Log("Visiting TGC+ companion website if it exists...")
        #coursePlusInfo = self.searchPlusURL(metadata.title, cNum)
        coursePlusInfo = None
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
                
        
        Log("Updating episode data")
        @parallelize
        def UpdateEpisodes(html=html, eSummaryData=eSummaryData, eTitleData=eTitleData, lecturer=lecturer):
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
                            def UpdateEpisode(episode=episode, html=html, episode_num=episode_num, eSummaryData=eSummaryData, eTitleData=eTitleData, lecturer=lecturer):
                                Log("def UpdateEpisode()")
                                lecture_len = len(eSummaryData)
                                lecture_len2 = len(eTitleData)
                                Log("Lecture array length: %s" % lecture_len)
                                if int(episode_num) <= lecture_len:
                                    Log("Episode Title: %s" % eTitleData[int(episode_num) - 1])
                                    Log("Episode summary %s" % eSummaryData[int(episode_num) - 1].strip())
                                    episode.title = str(eTitleData[int(episode_num) - 1 ])
                                    episode.summary = str(eSummaryData[int(episode_num) - 1].strip())
                                    if episode.rating is None:
                                        episode.rating = float(rating)
                                    Log("episode.summary: %s" % episode.summary)
                                    Log("episode.title: %s" % episode.title)
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
                                        
                                    Log("Getting Lecturer")
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
                Log("getting Art images")
                    
                    
        #episode.rating = rating
        Log("Downloading Art")
        @parallelize
        def DownloadArt(html=html):
            Log("DownloadArt()")
            art = [ ]
            Art = { }
            soup = BeautifulSoup(html)
            for link in soup.findAll("a", "cloud-zoom-gallery lightbox-group"):
                art.append(link.get('href'))
            Art['fanart'] = art[0]
            Art['poster'] = art[1]
            Log("Fanart URL: %s" % Art['fanart'])
            Log("Poster URL: %s" % Art['poster'])
            if Art['poster'] not in metadata.posters:
                @task
                def DownloadPoster(poster_url=Art['poster']):
                    Log("Downloading posters")
                    try:
                        metadata.posters[poster_url] = Proxy.Preview(HTTP.Request(poster_url).content, sort_order=1)
                    except: 
                        Log("Download of poster image failed! - %s" % poster_url)
                        pass
            else:
                Log("Poster art already in metadata.posters")
            metadata.posters.validate_keys(Art['poster'])
            
            if Art['fanart'] not in metadata.art:
                @task
                def DownloadFanArt(fanart_url=Art['fanart']):
                    Log("Downloading fanart")
                    try:
                        metadata.art[fanart_url] = Proxy.Preview(HTTP.Request(fanart_url).content, sort_order=1)
                    except: 
                        Log("Download of fanart image failed! - %s" % fanart_url)
                        pass
            else:
                Log("Fanart already in metadata.art")                        
            metadata.art.validate_keys(Art['fanart'])
            
        Log("Done")    
        return