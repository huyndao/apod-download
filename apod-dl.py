#!/usr/bin/env python3
# Copyright © 2023, Huy Dao
import requests
import re
import os, time, random
import argparse
import json
from tqdm.auto import tqdm, trange
from bs4 import BeautifulSoup
import requests.packages.urllib3

requests.packages.urllib3.disable_warnings()


def get_apod(url, adir):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; rv:84.0) Gecko/20100101 Firefox/84.0"
    }
    sess = requests.Session()
    if not os.path.exists(adir):
        os.makedirs(adir, exist_ok=False)

    parenturl = os.path.split(url)[0]
    spaceregex = re.compile(r"\s{2,}")

    print(f"getting image from {url}")
    apod = sess.get(url, timeout=30, headers=headers, verify=True)
    apod.raise_for_status()

    apodsoup = BeautifulSoup(apod.text, features="lxml")
    apod.close()

    imgelem = apodsoup.find_all("a", href=re.compile("^image"))

    if imgelem == []:
        print("No image link found\n")
    else:
        imgurl = parenturl + "/" + imgelem[0].get("href")
        imgfilename = os.path.basename(imgurl)
        imgdate = imgelem[0].find_previous("p").getText(strip=True)
        imgtitle = imgelem[0].find_next("b").getText(strip=True)
        imgtext = imgelem[0].find_next("p").getText()
        imgtext = re.sub("\n", " ", imgtext).strip()
        imgtext = re.sub(spaceregex, " ", imgtext)

        with open(os.path.join(adir, "album_list.txt"), "at") as albumfd:
            print(f'save album list to {os.path.join(adir, "album_list.txt")}')
            albumfd.write(
                imgdate
                + " - "
                + imgfilename
                + " - "
                + imgtitle
                + " - "
                + imgtext
                + "\n\n"
            )
            print(f"{imgdate} - {imgurl} --> {os.path.join(adir, imgfilename)}")
            if not os.path.exists(os.path.join(adir, imgfilename)):
                imageresp = sess.get(
                    imgurl,
                    headers=headers,
                    timeout=30,
                    cookies=apod.cookies,
                    stream=True,
                    verify=True,
                )
                total = int(imageresp.headers.get("content-length", 0))
                print(total)
                imageresp.raise_for_status()
                with open(os.path.join(adir, imgfilename), "wb") as fd:
                    for chunk in tqdm(
                        imageresp.iter_content(chunk_size=1024),
                        total=total / 1024,
                        unit="kiB",
                        unit_scale=True,
                        unit_divisor=1024,
                    ):
                        # print(".", end="", flush=True)
                        fd.write(chunk)
                    print("\n")
                    fd.flush()
                imageresp.close()
            else:
                print(f"file {imgfilename} already downloaded\n")
            albumfd.flush()

    try:
        prevlink = parenturl + "/" + apodsoup.find_all("a", string="<")[0].get("href")
    except Exception as exc:
        print(f"Can not find previous link")

    sess.close()
    return prevlink


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "-u",
        "--url",
        required=False,
        type=str,
        help="start url.  Start from this page.  If omitted, will start with today's page",
    )
    ap.add_argument(
        "-d",
        "--dir",
        required=False,
        type=str,
        help="name of directory to save files to.  If omitted, will create and save files to ./apod-images/",
    )
    ap.add_argument(
        "-o",
        "--oneday",
        required=False,
        action="store_true",
        help="just get the one day's apod and nothing else",
    )
    args = ap.parse_args()

    if args.url:
        url = args.url
    else:
        url = "https://apod.nasa.gov/apod/astropix.html"

    if args.dir:
        SAVEDIR = args.dir
    else:
        SAVEDIR = "apod-images"

    if args.oneday:
        _ = get_apod(url, SAVEDIR)
    else:
        while url:
            url = get_apod(url, SAVEDIR)

            # sleep randomly between 0 to 3 seconds
            time.sleep(random.randint(0, 3))
