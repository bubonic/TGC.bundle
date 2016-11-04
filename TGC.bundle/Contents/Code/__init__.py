from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint
from BeautifulSoup import BeautifulSoup 

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

TGC_COURSE_URL = 'http://www.thegreatcourses.com/courses/'
# For Sure yo
class TGCAgent(Agent.TV_Shows):
    
    name = 'TGC'
    
    class MyDESCParser(HTMLParser):
        def __init__(self):
            HTMLParser.__init__(self)
            self.recording = 0
            self.data = []

        def handle_starttag(self, tag, attributes):
            if tag != 'div':
                return
            if self.recording:
                self.recording += 1
                return
            for name, value in attributes:
                if name == 'class' and value == 'course-description':
                    break
            else:
                return
            self.recording = 1

        def handle_endtag(self, tag):
            if tag == 'div' and self.recording:
                self.recording -= 1

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
                self.recording += 1
                return
            for name, value in attributes:
                if name == 'class' and value == 'lecture-title':
                    break
            else:
                return
            self.recording = 1

        def handle_endtag(self, tag):
            if tag == 'div' and self.recording:
                self.recording -= 1

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
                self.recording += 1
                return
            for name, value in attributes:
                if name == 'class' and value == 'lecture-description-block left' or value == 'lecture-description-block right':
                    break
            else:
                return
            self.recording = 1

        def handle_endtag(self, tag):
            if tag == 'a' and self.recording:
                self.recording -= 1
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
                self.c2 = chr(int(name))
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
                self.recording += 1
                return
            for name, value in attributes:
                if name == 'class' and value == 'name':
                    break
            else:
                return
            self.recording = 1

        def handle_endtag(self, tag):
            if tag == 'span' and self.recording:
                self.recording -= 1

        def handle_data(self, data):
            if self.recording:
                self.data.append(data.strip())