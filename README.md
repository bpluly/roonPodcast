# roonPodcast
Command line application to add Podcasts to a folder with metadata with media so they can be streamed by Roon

### Command line arguments
url, destination [switches]

_url_ is the full url with any arguments of the podcast episode,

 _destination_ is the folder to place the metadata and content of the podcast.
 
_series_ is the product name of the podcast, or actually the series of the product if that makes sense. If there are spaces in the name then enclose the name in quotes ("")

Switches

`--artist` is the artist or artists for the podcast, this is often missing from podcast metadata

`--episodes` the number of episodes to collect. RSS feeds are in most recent order, using 1 for episodes it will collect the last one. 1 is the default.



