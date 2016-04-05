import pyquizlet
import requests
import json
import urllib2
import google, os
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

def quizletSearch(query):
    TEMPLATE = "https://api.quizlet.com/2.0/search/sets?client_id=3GbCW6xc9K&whitespace=1&q=%(query)s"
    url = TEMPLATE%{"query":query}
    request = urllib2.urlopen(url)
    result = request.read()
    r = json.loads(result)
    all_sets = []
    for sets in r["sets"][:5]:
        all_sets.append(("https://quizlet.com"+sets["url"]).encode("utf8"))
    return all_sets

def youtubeSearch(query):
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"
    DEVELOPER_KEY = "AIzaSyB-lhoDNkPGAFM-JT8ec1jLMe1cf4vA7J4"
    
    args = argparser.parse_args()
    options = args
    
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    search_response = youtube.search().list(q=query,part="id,snippet", maxResults=5).execute()
    videos = []
    counter = 0
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos.append([search_result["snippet"]["title"].encode("utf8"),(search_result["id"]["videoId"]).encode("utf8"), "player"+str(counter)])
            #, search_result["snippet"]["thumbnails"]["default"]['url']])
        counter+=1
    return videos

def getSources(): #Putting all Outside Sources into list 'srcs'
    srcs = []
    f = open(os.path.join(os.path.dirname(__file__), "misc/sources.txt"), "r")
    for line in f:
        line = line[0:-1] #-1 is to remove the newline character
        line = line.replace("https","")
        line = line.replace("http","")
        line = line.replace("//","")
        line = line.replace(":","")
        line = line.replace("www.","")
        srcs.append(line)
    return srcs

def googleSearch(query):
    l = []
    srcs = getSources()
    results = google.search(query,num=30,start=0,stop=1)
    for url in results:
        for src in srcs:
            if url.find(src)!=-1:
                l.append((url).encode("utf8"))
        #message = ""
        #    if (len(l)<2):
        #        message = "Timed Out: More results would take too long"
    return l

def searchAll(query):
    quizlet = quizletSearch(query)
    youtube = youtubeSearch(query)
    google = googleSearch(query)
    
    results = []
    count = 0
    while (count < 10):
        try:
            results.append(quizlet[count])
        except:
            print "Out of Quizlet"
        try:
            results.append(youtube[count])
        except:
            print "Out of Youtube"
        try:
            results.append(google[count])
        except:
            print "Out of Google"
        count += 1
    return results
    
#print searchAll("biology")
