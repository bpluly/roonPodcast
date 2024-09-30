#python3
#Imports podcast files for Roon

import feedparser
import requests



def fetchPodcast(url):
  feedparser.USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
  return feedparser.parse(url)













if __name__ == '__main__':
  #Main get the command line arguments and call processPodcast
  parser = argparse.ArgumentParser(description='Import a podcast into a folder that Roon can stream from.')
  parser.add_argument('url', metavar='S', type=string,
                    help='URL of the podcast')
  parser.add_argument('destination', metavar='S', type=string,
                     help='folder to place the podcast')
