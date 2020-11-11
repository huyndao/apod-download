# apod-download:  Download pictures from NASA's APOD (Astronomy Picture of the Day) site
## Usage:

All images will be downloaded to a directory named **apod-images**.  If directory does not exist, the script will create one.
Additionally, the image filename, image date and image text will be written to file: **apod-images/album\_list.txt**

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

## Requirement:
- python3
- requests
- beautifulsoup4
- argparse

