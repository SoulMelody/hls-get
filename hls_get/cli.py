import asyncio
from itertools import zip_longest

import click
from aiohttp.http import HeadersParser

from hls_get.downloader import HLSDownloader


async def download(links, path, names, coros, headers, clean_up):
    headers_parser = HeadersParser()
    header_lines = [b'', *(line.encode('latin-1') for line in headers), b'']
    parsed_headers, raw_headers = headers_parser.parse_headers(header_lines)
    for link, name in zip_longest(links, names):
        async with HLSDownloader(
            link, path, name, coros,
            headers=parsed_headers,
            clean_up=clean_up
        ) as downloader:
            await downloader.download(link)
            downloader.on_success()


@click.command(
    help='Download m3u8 links '
         '(like "http://www.example.domain/path/to/index.m3u8#Save name" '
         ' etc.) asynchronously, and merge into mp4 files.'
)
@click.argument('links', nargs=-1, required=True)
@click.option('-P', '--path', default='.', help='Save path')
@click.option('-N', '--names', multiple=True, help='Save name')
@click.option('-C', '--coros', default=5, help='Max coroutines')
@click.option('-H', '--headers', multiple=True, help='Headers parameters like curl\'s')
@click.option('-c', '--clean-up', default=True, help='Clean up the cache directory when completed', is_flag=True)
@click.option('-D', '--delay', default=3, help='delay seconds before retrying')
@click.option('-R', '--retry-times', default=10, help='Max retry times')
def main(*args, delay=3, retry_times=10, **kwargs):
    try:
        import uvloop
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    except ImportError:
        pass
    loop = asyncio.get_event_loop()
    loop.run_until_complete(download(*args, **kwargs))


if __name__ == '__main__':
    main()
