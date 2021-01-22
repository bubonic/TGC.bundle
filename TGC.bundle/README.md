# The Great Courses - PLEX Metadata Agent
This agent plug-in will organize your Great Courses with metadata for Course Summary, Lecture Titles, Lecture Summary, Course Rating, Professor Art, Professor Descriptiion, Cover and Background art as well. It makes viewing The Great Courses much easier and provides a nice interface to organize these great tools of learning!

The agent makes use of many shared libraries including Selenium, Whichcraft, pyvirtualdisplay (for linux Xvfb and Selenium operation), easyprocess, BeautifulSoup4 and urllib3. All sources are included in the *sources* directory. Also, the appropriate Selelnium/Firefox/Geckodriver stack for Linux users is included in the *packages* directory. 

## NOTE
You must use **Firefox 60.0** and **Geckodriver 0.26**. Newer Firefox versions may not work with the Selenium suite that this agent uses (**Selenium 3.141.0**). It was very time consuming to find the appropriate versions of Selenium, Firefox and Geckodriver that all worked together on a Linux Machine.

# Requirements
## Linux
- X11 or Xvfb (headless)
- ImageMagick 
- Geckodriver (included) [link](https://github.com/mozilla/geckodriver/releases/tag/v0.26.0)
- Firefox (included)     [link](https://ftp.mozilla.org/pub/firefox/releases/60.0/linux-x86_64/en-US/)

## Windows
- ImageMagick [link](https://imagemagick.org/script/download.php#windows)
- Geckodriver
- Firefox 60.0 [link](https://ftp.mozilla.org/pub/firefox/releases/60.0/)
- Geckodriver 0.26 [link](https://github.com/mozilla/geckodriver/releases/tag/v0.26.0)

# INSTALL

Download the complete contents of this git project (git clone) and copy the bundle (TGC.bundle) to your PLEX plug-ins directory.
The appropriate plug-ins directory can be found on the PLEX website (https://support.plex.tv/hc/en-us/articles/201106098-How-do-I-find-the-Plug-Ins-folder-)
Besure to restart the PLEX server after copying the Agent plug-in. 

## IMPORTANT
You must edit **line 38** of the code to tell us where your **Firefox 60.0** binary is located. That is edit the following line:

> FIREFOX = "/usr/local/bin/firefox/firefox"

For windows users it would be something like the following
 
> FIREFOX = "C:\firefox\firefox"

For Linux users you can keep the line in tact and install your Firefox 60.0 into the /usr/local/bin directory or edit it appropriately to point to wherever you installed that specific Firefox version.

 

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

## IMPORTANT
Currently the agent does not have a SearchCourse() function. This will be implemented shortly. It is *advised* that you name your courses as they appear in the TGC website url. The agent uses a "URL Guesser" to assume where to find the course and this is based off of how your course is named.

# VERY IMPORTANT
It is **strongly advised** that you do not load a directory with 500 courses directly into the Agent. This will cause either your server to back up and freeze or worse. The way I handle it is I do **5** course directories at a time. Although, it will take you longer to get everything in place, what is the rush? Watch a course while you do this. 

The most common scenario in the code of the *TGC.bundle* is that after 1 hour of getting course metadata, if there are any subsequent courses that still have yet to get metadata, the Agent will quit on you. Forcing you to manually refresh the metadata. No biggie, it's just checks in place to ensure low resource usage and memory consumption. 

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


# Donations

## PayPal
This agent was was very time consuming to create and if you are obliged in offering a donation please click on the following PayPal link

[![paypal](https://i.imgur.com/KSkRsgR.png)](https://www.paypal.com/donate?hosted_button_id=6LXBPHPTDDX56)

## Bitcoin
If you wish to remain anonymous and want to donate via Bitcoin, please send any amount to the following address:

**16h8ZqQpa3niwPWjTgtY584R7Z2txYGkYL**

## Monero

**89vAxHU8L9fYwa6KCT8TwX63Y5vaGhikz1o2zqJbjj8mKrhogY9PBEmiCcTxity2NjPCa6HsQ1gjnJH3WCBKWDjjHj5Q9F7**
