#python3
#Imports podcast files for Roon

import argparse
import feedparser
import requests
from pathlib import PurePath
from pprint import pprint
import sys


def fetchPodcast(url):
  feedparser.USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
  return feedparser.parse(url)

def processRequest(url, destination, series, parseFolder, artists, episodes):
  """ Main process that collects the podcast RSS using fetchPodcast and creates the structure for the file.
      It gets the mpg (or any other media file) into a file like variable from getMedia().
      It gets any images in the same way from getImages.
      It either navigates to the parsed folder for the Named Podcast or it builds the tree, and then creates
      the collected files.
      It then parses the metadata for the podcast and stores it as ID3 properties using putID3()
  """
  podcastStruct = fetchPodcast(url)
  for i in range(0,episodes - 1):
    entry = podcastStruct['entries'][i]
    podcast = {}
    podcast['title'] = entry['title']
    if artists == 'Artist':
      podcast['artist'] = entry['author']
    else:
      podcast['artist'] = artists
    if series != "":
      podcast['series'] = series
      
    for link in entry['links']:
      print(f"Link {link['type']} begins with {link['type'].startswith('audio')}")
      if 'type' in link:
        print('Creating image path')
        if link['type'].startswith("audio"):
          urlMain = link['href'].split('?')[0]
          print(f'urlMain:{urlMain}')
          image = urlMain.split('/')[-1]
          print(f'image:{image}')
          local_file = PurePath(destination, series, image)
          print(f'local_file {local_file}')
          response = requests.get(link['href'], stream=True)
          with open(local_file, 'wb') as f:
              for chunk in response.iter_content(chunk_size=1024): 
                  if chunk: # filter out keep-alive new chunks
                      f.write(chunk)
          print(f'Written {local_file}')
 


if __name__ == '__main__':
  #Main get the command line arguments and call processPodcast
  sys.stdin.reconfigure(encoding='utf-8')
  sys.stdout.reconfigure(encoding='utf-8')
  parser = argparse.ArgumentParser(description='Import a podcast into a folder that Roon can stream from.')
  parser.add_argument('url', help='URL of the podcast')
  parser.add_argument('destination', help='folder to place the podcast')
  parser.add_argument('series', default="", help='Series to place episodes.')
  parser.add_argument('--artist', default='Artist', help='Set the Artist for the podcast.')
  parser.add_argument('--episodes', type=int, default=1,
                     help='How many episodes to fetch, the default is 1.')
  args = parser.parse_args()
  
  processRequest(args.url, args.destination, args.series, args.parseFolder, args.artist, args.episodes)
