from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint
from BeautifulSoup import BeautifulSoup 
import datetime
import sys


try:
    # For Python 3.0 and later
    from urllib.request import urlopen
    import urllib
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen
    import urllib2
    
try: 
    import dryscrape
except ImportError:
    Log("Can't continue, need the dryscrape module to continue")


TGC_COURSE_URL = 'http://www.thegreatcourses.com/courses/'
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0'
ONE_DAY = datetime.timedelta(days=1)
TODAY = datetime.date.today()

# For Sure yo

def Start():

    HTTP.CacheTime = CACHE_1DAY
    
class TGCAgent(Agent.TV_Shows):
    
    name = 'TGC'
    languages = [Locale.Language.English]
    primary_provider = True
    accepts_from = ['com.plexapp.agents.localmedia']

#    accepts_from = ['com.plexapp.agents.localmedia']
    
    
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
            self.switch = 0

        def handle_starttag(self, tag, attributes):
            if tag != 'div':
                return
            if self.recording:
                self.recording = self.recording + 1
                return
            for name, value in attributes:
                if name == 'class' and value == 'lecture-title':
                    break
            else:
                return
            self.recording = 1

        def handle_endtag(self, tag):
            if tag == 'div' and self.recording:
                self.recording = self.recording - 1

        def handle_data(self, data):
            if self.recording:
                if data and data != 'x' and data != ' ':
                    if self.switch == 1:
                        last = self.data.pop()
                        self.newdata = ' '. join([last, data])
                        self.data.append(self.newdata)
                        self.switch = 0
                    else:
                        self.data.append(data)

        def handle_entityref(self, name):
            self.c = unichr(name2codepoint[name])
            if self.data and self.recording:
                last = self.data.pop()
                self.newdata = ' '.join([last,self.c])
                self.data.append(self.newdata)
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
                        self.newdata = ' '. join([last, data])
                        self.data.append(self.newdata)
                        self.switch = 0
                    else:
                        data.strip()
                        self.data.append(data)


        def handle_entityref(self, name):
            self.c = unichr(name2codepoint[name])
            if self.data and self.recording:
                last = self.data.pop()
                self.newdata = ' '.join([last,self.c])
                self.data.append(self.newdata)
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
                self.newdata2 = ' '.join([last,self.c2])
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
        rHTML = soup.find(itemprop='ratingValue')
        rating = rHTML.getText()
        return float(rating)
    
    def getDESC(self, html):
        DESC = ''
        COUNTER = 1
        
#        request = urllib2.Request(courseURL)
#        request.add_header('User-Agent', USER_AGENT)
#        opener = urllib2.build_opener()
#        html = opener.open(request).read()
        parser = self.MyDESCParser()
        parser.feed(html)
        data = parser.data
        
        for desc in data:
            if COUNTER < 20:
                if not desc.isspace():
                    DESC = ''.join([DESC,desc])
                    COUNTER += 1
            else:
                break
        
        return DESC.strip()
    
    def search(self, results, media, lang, manual=False):
        id2 = media.show
        show = media.show.lower()
        show = show.replace(' ', '-')
        show = show.replace(':', '')
        show = show.replace(',', '')
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
        show = metadata.id
        show = show.lower()
        show = show.replace(' ', '-')
        show = show.replace(':', '')
        show = show.replace(',', '')
        courseURL = ''.join([TGC_COURSE_URL, show, '.html'])
        Log("update() CourseURL: %s" % courseURL)
        Log("Calling dryscrape and visiting coursURL")
        #session = dryscrape.Session()
        #session.set_header('User-Agent', USER_AGENT)
        #session.visit(courseURL)
        #html = session.body()
        
        #Log("Getting Rating")
        #r = self.getRating(html)
        #rating = 2*r
        
        Log("calling urllib2 and visiting coursURL")
        request = urllib2.Request(courseURL)
        request.add_header('User-Agent', USER_AGENT)
        opener = urllib2.build_opener()
        html = opener.open(request).read()

        data = self.getDESC(html)
        Log("Adding metadata summary")
        metadata.summary = data
        #Log("Retrieving episode/season number")
        #season_num = media.season
        #episode_num = media.episode
        Log("Updating episode data")
        if media is not None:
            Log("Media is not None")
            for season_num in media.seasons:
                Log("Season Number:%s" % season_num)
                for episode_num in media.seasons[str(season_num)].episodes:
                    Log("Episode number:%s" % episode_num)
                    episode = metadata.seasons[str(season_num)].episodes[str(episode_num)]
                    Log("Running UpdateEpisode...see if this works")
                    parser = self.MyLDESCParser()
                    parser2 = self.MyLTITLEParser()
                    parser.feed(html)
                    parser2.feed((html))
                    eSummaryData = parser.data
                    eTitleData = parser2.data
                    Log("Episode Title: %s" % eTitleData[0])
                    Log("Episode summary %s" % eSummaryData[0].strip())
                    episode.summary = str(eSummaryData[0].strip())
                    episode.title = str(eTitleData[0])
                    Log("episode.summary: %s" % episode.summary)
                    Log("episode.title: %s" % episode.title)
        #episode.rating = rating
        Log("Done")
        return