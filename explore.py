import pyquizlet
import requests
import json
import urllib2
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
DEVELOPER_KEY = "AIzaSyB-lhoDNkPGAFM-JT8ec1jLMe1cf4vA7J4"

def quizletSearch(query):
    TEMPLATE = "https://api.quizlet.com/2.0/search/sets?client_id=3GbCW6xc9K&whitespace=1&q=%(query)s"
    url = TEMPLATE%{"query":query}
    request = urllib2.urlopen(url)
    result = request.read()
    r = json.loads(result)
    all_sets = []
    for sets in r["sets"]:
        all_sets.append([sets["title"],"https://quizlet.com"+sets["url"]])
    return all_sets

def youtubeSearch(query):
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"
    
    argparser.add_argument("--q", help="Search term", default=query)
    argparser.add_argument("--max-results", help="Max results", default=10)
    args = argparser.parse_args()
    options = args
    
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    search_response = youtube.search().list(q=options.q,part="id,snippet", maxResults=options.max_results).execute()
    videos = []
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos.append([search_result["snippet"]["title"],"https://www.youtube.com/watch?v=" + search_result["id"]["videoId"]])
            #, search_result["snippet"]["thumbnails"]["default"]['url']])
    return videos

def googleSearch(q):
    pass

def searchAll(query):
    quizlet = quizletSearch(query)
    youtube = youtubeSearch(query)
    #google = googleSearch(query)
    
    results = []
    count = 0
    while (count < 10):
        results.append(quizlet[count])
        results.append(youtube[count])
        #results.append(google[count])
        count += 1
    return results
    
#print searchAll("biology")
