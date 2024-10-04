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

### Use
If the destination folder is in the tree that Roon scans for music files or changes in the catalogue then it will be added to the Library. Whilst there is no individual UI for podcasts they do contain the tag _genre_ podcast and can be selected from the Genres menu.
This doesn't give subscriptions to podcasts or RSS feeds wrapping _roonPodcast_ in a batch file or shell script and then adding that to crontab or Task Scheduler will give you an effective subscription.



