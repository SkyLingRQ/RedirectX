import aiohttp
import asyncio
import argparse
from urllib.parse import urlparse, urlencode, parse_qs, urlunparse
from colorama import init, Fore

init()

green = Fore.GREEN
reset = Fore.RESET

parse = argparse.ArgumentParser(description="")
parse.add_argument('-u', '--url', help="")
parse.add_argument('-l', '--list', help="")

args = parse.parse_args()


async def scan(url, session):
    try:
        async with session.get(url, allow_redirects=True) as response2:
            response2 = str(response2.url)
            if response2.startswith("https://www.google.com/"):
                print(f"{green}[ VULNERABLLE ] {url}{reset}")
            else:
                pass
    except Exception:
        pass
async def main():
    async with aiohttp.ClientSession() as session:
        task = []

        if args.url:
            urlparsed = urlparse(args.url)
            query = parse_qs(urlparsed.query)
            for key in query:
                query[key] = ["https://www.google.com/"]
                queryencoded = urlencode(query, doseq=True)
                urlFull = urlunparse(urlparsed._replace(query=queryencoded))
                task.append(scan(urlFull, session))

        if args.list:
            with open(args.list, 'r') as rf:
                urls = rf.readlines()
            for url in urls:
                url_parsed = urlparse(url.strip())
                qs = parse_qs(url_parsed.query)
                for key in qs:
                    qs[key] = ["https://www.google.com/"]
                    new_query = urlencode(qs, doseq=True)
                    newUrl = urlunparse(url_parsed._replace(query=new_query))
                    task.append(scan(newUrl, session))
        
        if task:
            await asyncio.gather(*task)

asyncio.run(main())
