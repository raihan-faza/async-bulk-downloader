import asyncio
import os
import sys
from urllib.parse import urlsplit

import aiofiles
import aiohttp
from pyfiglet import Figlet
from tqdm import tqdm


def folder_check(folder_path: str):
    if os.path.exists(folder_path):
        return
    os.makedirs(folder_path)


async def create_download_coroutine(
    session: aiohttp.ClientSession,
    url: str,
    save_loc: str,
):
    folder_check(save_loc)
    file_name = os.path.basename(urlsplit(url).path)
    async with session.get(url) as res:
        if res.status == 200:
            file = await aiofiles.open(save_loc + "/" + file_name, "wb")
            await file.write(await res.read())
            await file.close()


async def main():
    f = Figlet(font="slant")
    print(f.renderText("Async-Bulk__D"))
    if len(sys.argv) != 3:
        print("Error: missing argument")
        print("Usage: python main.py url_list_file desired_folder_path")
        print("Example: python main.py lahh.txt /home/lahh/")
        print("Example: python main.py lahh.txt lahh")
        sys.exit(1)
    url_list = sys.argv[1]
    folder_to_save = sys.argv[2]
    with open(url_list, "r") as f:
        url_list = [x.strip("\n") for x in f.readlines()]
    async with aiohttp.ClientSession() as session:
        download_coroutines = [
            create_download_coroutine(session, url, folder_to_save) for url in url_list
        ]
        for prog in tqdm(
            asyncio.as_completed(download_coroutines),
            total=len(download_coroutines),
            desc="Downloading",
            unit="file",
        ):
            await prog


if __name__ == "__main__":
    asyncio.run(main())
