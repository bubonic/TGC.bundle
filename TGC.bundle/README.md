# Requirements

For now, this PLEX Agent requires urllib/urllib2 and BeautifulSoup to run. I believe the PLEXmediaserver comprises of these libraries already in the bundle, so there should be no need to download themm. 

# INSTALL

Download the complete contents of this git project (git clone) and copy the bundle (TGC.bundle) to your PLEX plug-ins directory.
The appropriate plug-ins directory can be found on the PLEX website (https://support.plex.tv/hc/en-us/articles/201106098-How-do-I-find-the-Plug-Ins-folder-)
Besure to restart the PLEX server after copying the Agent plug-in. 

# Usage

You can choose between two file naming schemes for your course files: 

1. FULL COURSE NAME S01E## Some Text.ext

or

2. FULL COURSE NAME (TGC####) S01E## Some text.ext

(where TGC#### is the course number found on the TGC website). If you choose 2. the Agent should always locate the course and download the necessary metadata. Also, adding the course number to the filenames as show above will result in a sure method of gathering the lecture thumbnails from the TGC+ website for available courses. Thus, it is best to name each lecture with the second method.  

and 

where E## is the lecture number. The Full Course name **should** be taken from TGC website.
The files **must** be renamed properly for this Agent to pull the data from TGC website.

From my understanding you can also rename the directory that contains the lectures to the full course name and have each subsequent lecture file be named S01E##.mp4 and the agent will still pull the data.

### Example:

Games People Play: Game Theory in Life, Business, and Beyond S01E01 The World of Game Theory.mp4

or

Change and Motion: Calculus Made Clear, 2nd Edition S01E10 Blah.avi

or

The Black Death: The World's Most Devastating Plague (TGC8241) S01E01.mp4

The FULL COURSE NAME can be found as the heading of the course webpage. 

Create a TV Shows Library in PLEX and set the primary agent to TGC.  i.e.,

![](http://i.imgur.com/MutBhRy.png "") 

![](http://i.imgur.com/daSfKiv.png "")
 
Add directories *individually* (not directories of directories) to your library and enjoy! i.e., 
I haven't yet tested if you can add a directory containing directories of lecture files. 

![](http://i.imgur.com/StVCbzk.png "")