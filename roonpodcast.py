#python3
#Imports podcast files for Roon

import feedparser
import requests



def fetchPodcast(url):
  feedparser.USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
  return feedparser.parse(url)

def processRequest(url, destination, parseFolder):
  """ Main process that collects the podcast RSS using fetchPodcast and creates the structure for the file.
      It gets the mpg (or any other media file) into a file like variable from getMedia().
      It gets any images in the same way from getImages.
      If the parseFolder is true then it either navigates to the parsed folder for the Named 
      Podcast or it builds the tree, and then creates the collected files.
      It then parses the metadata for the podcast and stores it as ID3 properties using putID3()
  """
  podcastStruct = fetchPodcast(url)
  



if __name__ == '__main__':
  #Main get the command line arguments and call processPodcast
  parser = argparse.ArgumentParser(description='Import a podcast into a folder that Roon can stream from.')
  parser.add_argument('url', metavar='S', type=string,
                    help='URL of the podcast')
  parser.add_argument('destination', metavar='S', type=string,
                     help='folder to place the podcast')
  parser.add_argument('--parseFolder', action='store_true',
                     help='Creates or maps the Podcast to a set of hierarchical folders, equivalent to an Artist and Album.')
  args = parser.parse_args()
  processRequest(args.url, args.destination, args.parseFolder )
