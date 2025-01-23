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


async def download(url: str, save_loc: str):
    file_name = os.path.basename(urlsplit(url).path)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            if res.status == 200:
                file = await aiofiles.open(save_loc + "/" + file_name, "wb")
                await file.write(await res.read())
                await file.close()


async def main():
    """
    f = Figlet(font="slant")
    print(f.renderText("Async-Bulk__D"))
    if len(sys.argv) != 3:
        print("Error: missing argument")
        print("Usage: python main.py url_list_file desired_folder_path")
        print("Example: python main.py lahh.txt /home/lahh/")
        print("Example: python main.py lahh.txt lahh")
        sys.exit(1)
    """
    url_list = sys.argv[1]
    folder_to_save = sys.argv[2]
    for url in tqdm(url_list):
        await download(url, folder_to_save)


if __name__ == "__main__":
    asyncio.run(main())
