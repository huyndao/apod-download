# apod-dl.py:  Download pictures from NASA's APOD (Astronomy Picture of the Day) site

## Description

All images will be downloaded to a directory named **apod-images**.  If directory does not exist, the script will create one.

Additionally, the image filename, image date and image text will be written to file: **apod-images/album_list.txt**


### Help
```bash
python3 apod-dl.py -h

usage: apod-dl.py [-h] [-u URL] [-o]

optional arguments:
  -h, --help         show this help message and exit
  -u URL, --url URL  start url. Start from this page
  -o, --oneday       just get the one day's apod and nothing else
```

### Sample Usage
#### Download everything from today's date and backward infinity:
```bash
python3 apod-dl.py 
```

#### Download from date's url and backward infinity:
```bash
python3 apod-dl.py -u "https://apod.nasa.gov/apod/ap201109.html"
```

#### Download today's picture only:
```bash
python3 apod-dl.py -o
```

#### Download date's picture only:
```bash
python3 apod-dl.py -o -u "https://apod.nasa.gov/apod/ap201109.html"
```

### Requirements
- python3
- requests
- beautifulsoup4
- argparse

