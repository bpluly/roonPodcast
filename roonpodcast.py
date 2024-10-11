#python3
#Imports podcast files for Roon

import argparse
import feedparser
import requests
import datetime
from dateutil import parser

from pathlib import PurePath, Path
from pprint import pprint
import sys, subprocess

MUTAGEN = "D:\Python311\Scripts\mid3v2.exe"
ARTIST = "--artist"
TRACK = "--track"

def fetchPodcast(url):
  feedparser.USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
  return feedparser.parse(url)
  
def validatePaths(destination, series):
  """ Validate the destination's existence, if it isn't then return False
      as it's really too messy to recover from.  If destination/series doesn't exist
      then create it and return True, if the creation fails return False
  """
  if Path(destination).exists() == False:
    print(f'The destination {destination} does not exist.')
    return False
  seriesPath =  Path(destination, series)
  if seriesPath.exists() == False:
    try:
      seriesPath.mkdir()
    except IOError as e:
      print(f'Failed to create {series}, exception {e}')
      return False
  return True
      
def setID3Property(file, property=None, value=None):
  """ Run the utility to set properties in the sound file.
  """
  if value != None:
    subprocess.call([MUTAGEN, file, property, value])
  
def useEpisodeWeek(podcast):
  """If there's a publish date then convert that to week number and return that.
     in future think a way of including the day in case there are multiple episodes
     in a week.
  """
  if 'published' in podcast:
    print(f"Published string is:{podcast['published']}")
    datePublish = parser.parse(podcast['published'])
    track = '%s-%s' % (datePublish.isocalendar().week, datePublish.isocalendar().weekday)
    return track
  else:
    print(f"published key not found")
    return None  #none doesn't break Roon but tracks become alphabetic of hashed names
  
def getMedia(link, destination, series):
  """ Get the media file and store it in the destination.
  """
  urlMain = link['href'].split('?')[0]
  print(f'urlMain:{urlMain}')
  image = urlMain.split('/')[-1]
  print(f'image:{image}')
  isValidPath = validatePaths(destination, series)
  if isValidPath == False:
    return None
  local_file = PurePath(destination, series, image)
  print(f'local_file {local_file}')
  response = requests.get(link['href'], stream=True)
  with open(local_file, 'wb') as f:
      for chunk in response.iter_content(chunk_size=1024): 
          if chunk: # filter out keep-alive new chunks
              f.write(chunk)
  print(f'Written {local_file}')
  return local_file
  

def processRequest(url, destination, series, artists, episodes):
  """ Main process that collects the podcast RSS using fetchPodcast and creates the structure for the file.
      It gets the mpg (or any other media file) into a file like variable from getMedia().
      It gets any images in the same way from getImages.
      It either navigates to the parsed folder for the Named Podcast or it builds the tree, and then creates
      the collected files.
      It then parses the metadata for the podcast and stores it as ID3 properties using putID3()
  """
  podcastStruct = fetchPodcast(url)
  for i in range(0,episodes):
    entry = podcastStruct['entries'][i]
    podcast = {}
    podcast['title'] = entry['title']
    if artists == 'Artist':
      podcast['artist'] = entry['author']
    else:
      podcast['artist'] = artists
    if series != "":
      podcast['series'] = series
    if 'published' in entry:
      podcast['published'] = entry['published']
    if 'itunes_episode' in entry:
      podcast['track'] = entry['itunes_episode']
    elif 'episode' in entry:
      podcast['track'] = entry['episode']
    else:
      podcast['track'] = useEpisodeWeek(podcast)
      print(f"Episode Week {podcast['track']}")
      
    for link in entry['links']:
      if 'type' in link:
        if link['type'].startswith("audio"):
          print('Getting audio.')
          soundFileName = getMedia(link, destination, series)
          setID3Property(soundFileName, property=ARTIST, value=podcast['artist'])
          setID3Property(soundFileName, property=TRACK, value=podcast['track'])


 


if __name__ == '__main__':
  #Main get the command line arguments and call processPodcast
  sys.stdin.reconfigure(encoding='utf-8')
  sys.stdout.reconfigure(encoding='utf-8')
  argParser = argparse.ArgumentParser(description='Import a podcast into a folder that Roon can stream from.')
  argParser.add_argument('url', help='URL of the podcast')
  argParser.add_argument('destination', help='folder to place the podcast')
  argParser.add_argument('series', default="", help='Series to place episodes.')
  argParser.add_argument('--artist', default='Artist', help='Set the Artist for the podcast.')
  argParser.add_argument('--episodes', type=int, default=1,
                     help='How many episodes to fetch, the default is 1.')
  args = argParser.parse_args()
  
  processRequest(args.url, args.destination, args.series, args.artist, args.episodes)
