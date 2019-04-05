import asyncio
from itertools import zip_longest

import click
from aiohttp.http import HeadersParser

from hls_get.downloader import HLSDownloader


async def download(links, path, names, coros, headers):
    headers_parser = HeadersParser()
    header_lines = [b'', *(line.encode('latin-1') for line in headers), b'']
    parsed_headers, raw_headers = headers_parser.parse_headers(header_lines)
    for link, name in zip_longest(links, names):
        async with HLSDownloader(link, path, name, coros, headers=parsed_headers) as downloader:
            await downloader.download(link)
            downloader.on_success()


@click.command(
    help='Download m3u8 links '
         '(like "http://www.example.domain/path/to/index.m3u8#Save name" '
         ' etc.) asynchronously, and merge into mp4 files.'
)
@click.argument('links', nargs=-1)
@click.option('-P', '--path', default='.', help='Save path')
@click.option('-N', '--names', multiple=True, help='Save name')
@click.option('-C', '--coros', default=5, help='Max coroutines')
@click.option('-H', '--headers', multiple=True, help='Headers parameters like curl\'s')
def main(*args, **kwargs):
    try:
        import uvloop
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    except ImportError:
        pass
    loop = asyncio.get_event_loop()
    loop.run_until_complete(download(*args, **kwargs))


if __name__ == '__main__':
    main()
