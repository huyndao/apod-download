# apod-download:  Download pictures from NASA's APOD (Astronomy Picture of the Day) site
## Usage:

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

