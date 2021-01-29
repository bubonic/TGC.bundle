# The Great Courses - PLEX Metadata Agent
This agent plug-in will organize your The Great Courses with metadata for Course Summary, Lecture Titles, Lecture Summary, Course Rating, Professor Art, Professor Descriptiion, Cover and Background art as well. It makes viewing The Great Courses much easier and provides a nice interface to organize these great tools of learning!

The agent makes use of many shared libraries including Selenium, Whichcraft, pyvirtualdisplay (for linux Xvfb and Selenium operation), easyprocess, BeautifulSoup4, urllib3, and python-Levenshtein - some of which had to be compiled on ancient PLEX python framework. All sources of the libraries are included in the *sources* directory. Also, the appropriate Selelnium/Firefox/Geckodriver stack for Linux users is included in the *packages* directory. 

## Note
If you are on Linux, *you must* use **Firefox 60.0** and **Geckodriver 0.26**. Newer Firefox versions may not work with the Selenium suite that this agent uses (**Selenium 3.141.0**). It was very time consuming to find the appropriate versions of Selenium, Firefox and Geckodriver that all worked together on a Linux Machine.

### Note 2 (Working Linux Model)
This has only been tested on Linux, Ubuntu 20.04 machine with the version *Version 1.21.1.3876* of the PLEX Media Server.
If it is not working or something wrong happens, Please review the agent and system logs of PLEX and post them in the issues section. 

### Note 3 (Working Windows Model)
As we work through the issues to get this agent working on all platforms, a user *jasper willems* has found the correct stack in achieving a working model for windows. Specifically, Firefox 52.8 for Windows 10 x64. Link for the correct Firefox for Windows 10 uers is below in the Windows Requirement section. Thanks *Jasper*

# Requirements
## Linux
- X11 or Xvfb (*sudo apt install xvfb*)
- ImageMagick (*sudo apt install imagemagick*)
- Geckodriver (included) [link](https://github.com/mozilla/geckodriver/releases/tag/v0.26.0)
- Firefox (included)     [link](https://ftp.mozilla.org/pub/firefox/releases/60.0/linux-x86_64/en-US/)

## Windows
- ImageMagick [link](https://imagemagick.org/script/download.php#windows)
- Firefox 52.8.1esr [link](https://ftp.mozilla.org/pub/firefox/releases/52.8.1esr/win64/en-GB/)
- Geckodriver 0.26 [link](https://github.com/mozilla/geckodriver/releases/tag/v0.26.0)

# INSTALL

Download the complete contents of this git project (git clone) and copy the bundle (TGC.bundle) to your PLEX plug-ins directory. Don't copy the git cloned directory; instead change to the git directory you just cloned (TGC.bundle) and copy the contents of the TGC.bundle directly from there. i.e.,

```
git clone https://github.io/bubonic/TGC.bundle
cd TGC.bundle
sudo cp -R TGC.bundle /var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Plug-ins
sudo chown -R plex.plex /var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Plug-ins/TGC.bundle
```

The appropriate plug-ins directory can be found on the PLEX website (https://support.plex.tv/hc/en-us/articles/201106098-How-do-I-find-the-Plug-Ins-folder-)
Besure to restart the PLEX server after copying the Agent plug-in. 

## IMPORTANT
You must edit **line 38** of the code to tell us where your appropriate Firefox binary is located. That is edit the following line:

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

From my understanding you can also rename the directory that contains the lectures to the full course name and have each subsequent lecture file be named S01E##.mp4 and the agent will still pull the data.

## IMPORTANT - Advanced Search Feature

With the full release of TGC.bundle v2.0 (h.l. mencken), I have compiled and utilized the Jaro-Levenshtein matching algorithm for use with a search course feature on TGC website. This allows a more lax naming scheme to be used if you don't want your time to be consumed looking up the full course name on TGC website and naming directories/files as such. 

The matching algorithm is very precise and will find the correct course 97% of the time based on the common directory names from the versions of the courses found online. You do still have to name the individual lectures like **S01E##** with **E##** as the correct lecture number in the series. 

## Cover art

I use ImageMagick for image pre and post processing in order to create an elegant course cover photo. It is also used as the background image for the course. Because TGC switched to landscape images, I had to create a workaround for making a poster image from that and that is why ImageMagick is now a new requirement. 

# VERY IMPORTANT
It is **strongly advised** that you do not load a directory with 500 courses directly into the Agent. This will cause either your server to back up and freeze or worse. The way I handle it is I do **5** (five) course directories at a time. Although, it will take you longer to get everything in place, what is the rush? Watch a course while you do this. 

The most common scenario in the code of the *TGC.bundle* is that after 1 hour of getting course metadata, if there are any subsequent courses that still have yet to get metadata, the Agent will quit on you; forcing you to manually refresh the metadata. No biggie, it's just checks in place to ensure low resource usage and low memory consumption. 

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

## Results

![](https://i.imgur.com/1ruis8a.png)

![](https://i.imgur.com/h1DQYPT.png)

![](https://i.imgur.com/ixyHsC5.png)

![](https://i.imgur.com/nNC1dkp.png)
# Donations

## PayPal
This agent was was very time consuming to create and if you are obliged in offering a donation please click on the following PayPal link

[![paypal](https://i.imgur.com/KSkRsgR.png)](https://www.paypal.com/donate?hosted_button_id=6LXBPHPTDDX56)

## Bitcoin
If you wish to remain anonymous and want to donate via Bitcoin, please send any amount to the following address:

**16h8ZqQpa3niwPWjTgtY584R7Z2txYGkYL**

## Monero

**89vAxHU8L9fYwa6KCT8TwX63Y5vaGhikz1o2zqJbjj8mKrhogY9PBEmiCcTxity2NjPCa6HsQ1gjnJH3WCBKWDjjHj5Q9F7**