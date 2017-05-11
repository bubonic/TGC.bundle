* Use the Plex Agent API instead of urllib2/BeautifulSoup to expand compatibility when parsing HTML.
✓ * Fix episode director/writer object to contain pulled Lecturer/Professor data.
* Clean up some of the code.
* Add more try/except error checking.
* Use JSON to pull rating from TGC website (currently only dryscrape compatability).
* Add checks for existing metadata so it's not updating the metadata every time.
* Make to code less demanding on the PLEX server.
