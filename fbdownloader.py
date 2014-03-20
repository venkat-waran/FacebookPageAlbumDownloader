#python script to download photos from facebook page
#Author Venkateswaran <venkates30@gmail.com>
import facebook
import urlparse
import urllib2
import os
import re

import argparse
graph = facebook.GraphAPI()
#destination directory to save the page
destdir="D:/Blake-Lively"
#facebook page id 
pagename = "449198405123854"
#download the given url to the given file location
def download(url,filename):
    try:
        print "Downloading "+filename
        f = open(filename,'wb')
        netfile = urllib2.urlopen(url,timeout=10)
        f.write(netfile.read())
        f.flush()
        f.close()
        print "Downloading complete for "+filename
    except:
        print "Downloading of "+filename+" failed"

#utility function that parses a given facebook albumm
#arguments
#url - facebook album id
#args - pagination number for downloading album , usually used in 
def parsealbum(url,args=None):
    print "Start parse album"
    albumid = ""
    r = re.compile('fbid=(.*?)&')
    m = r.search(url)
    if m:
        albumid = m.group(1)
    #print "album id is"+albumid
    if args!=None:
        images = graph.get_object(albumid+"/photos",after=args)
    else:
         images = graph.get_object(albumid+"/photos")
    for image in images['data']:
        for img in image['images']:
            #print img['source']
            image_url = img['source']
            image_name = img['source'].split('/')[-1]
            download(image_url,destdir+"/"+image_name)
            break
    if "next" in images['paging']:        
        next_page =  images['paging']['next']
        print next_page
        par = urlparse.parse_qs(urlparse.urlparse(next_page).query)
        next_page_id = par['after'][0]
        print "Next page's id is "+str(next_page_id)
        parsealbum(url,next_page_id)

parser = argparse.ArgumentParser()
parser.add_argument("fbpageurl", help="facebook page's url i.e https://facebook.com/page/....")
parser.add_argument("destinationdir", help="destination directory to store the downloaded photos")
args = parser.parse_args()
args.fbpageurl
facebook_page_pattern = r'https://www.facebook.com/pages/.*'
if re.match(facebook_page_pattern,args.fbpageurl):
    pass
else:
    print "The facebook page url you have specified is not  proper "
    exit(1)
pagename = args.fbpageurl.split('/')[-1]   

if os.path.isdir(args.destinationdir):
    destdir = args.destinationdir
else:
    print "Destination directory "+args.destinationdir+" does not exist.."
    exit(1)


page = graph.get_object(pagename+"/albums")
for data in page['data']:
    #print data['link']
    parsealbum(data['link'])
    #break
#print page['next']
#print str(vars(page))
