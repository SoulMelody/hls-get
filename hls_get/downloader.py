import asyncio
import binascii
import os
import shutil

import aiofiles
import aiohttp
import backoff
import click
import m3u8
from Cryptodome.Cipher import AES
from progress.bar import Bar
from yarl import URL

from hls_get.remuxer import remux


class HLSDownloader:
    def __init__(self, link, path, name, coros, **kwargs):
        self.session = aiohttp.ClientSession(trust_env=True, **kwargs)
        url = URL(link)
        self.name = name or os.path.basename(url.fragment or link)
        self.sem = asyncio.Semaphore(coros)
        self.path = path
        self.key_cache = dict()

    async def __aenter__(self):
        await self.session.__aenter__()
        return self

    async def __aexit__(self, *args):
        await self.session.__aexit__(*args)

    @property
    def cache_dir(self):
        return f'{self.path}/{self.name}'

    def on_success(self):
        remux(f'{self.cache_dir}/filelist.m3u8', self.name)
        clean_up = click.confirm('Clean up the cache directory?')
        if clean_up:
            shutil.rmtree(self.cache_dir)

    @backoff.on_exception(backoff.expo, Exception, max_tries=3)
    async def fetch_with_retry(self, link):
        async with self.sem, self.session.get(link) as resp:
            resp.raise_for_status()
            return await resp.read()

    async def download_segment(self, seq_num, segment, bar):
        filename = f'{self.cache_dir}/{seq_num}.ts'
        if not os.path.exists(filename):
            content = await self.fetch_with_retry(segment.absolute_uri)
            key = segment.key
            if key is not None and key.method == 'AES-128':
                if key.absolute_uri not in self.key_cache:
                    self.key_cache[key.absolute_uri] = await self.fetch_with_retry(key.absolute_uri)
                iv = key.iv or binascii.a2b_hex('%032x' % seq_num)
                cipher = AES.new(self.key_cache[key.absolute_uri], AES.MODE_CBC, iv=iv)
                content = cipher.decrypt(content)
            async with aiofiles.open(filename, 'wb') as piece:
                await piece.write(content)
        bar.next()

    async def download(self, link):
        async with self.sem, self.session.get(link) as resp:
            resp.raise_for_status()
            m3u8_obj = m3u8.loads(await resp.text(), uri=resp.url.human_repr())
            if not m3u8_obj.media_sequence:
                if m3u8_obj.is_variant:
                    for i, playlist in enumerate(m3u8_obj.playlists):
                        click.echo(
                            f'{i}: bandwidth={playlist.stream_info.bandwidth} '
                            f'resolution={playlist.stream_info.resolution} '
                            f'codecs={playlist.stream_info.codecs} '
                        )
                    index = click.prompt(
                        'Which playlist to download?',
                        type=click.Choice(list(range(len(m3u8_obj.playlists)))),
                        value_proc=int,
                        default=0
                    )
                    return await self.download(m3u8_obj.playlists[index].absolute_uri)
                else:
                    tmp_list = m3u8.M3U8()
                    tmp_list.version = '3'
                    tmp_list.media_sequence = '0'
                    tmp_list.target_duration = m3u8_obj.target_duration
                    tmp_list.is_endlist = True
                    tasks = []
                    os.makedirs(self.cache_dir, exist_ok=True)
                    bar = Bar(self.name, max=len(m3u8_obj.segments))
                    for i, segment in enumerate(m3u8_obj.segments):
                        tmp_list.add_segment(
                            m3u8.Segment(
                                f'{os.path.realpath(self.cache_dir)}/{i}.ts',
                                duration=segment.duration,
                                base_uri='file://'
                            )
                        )
                        tasks.append(
                            asyncio.ensure_future(
                                self.download_segment(i, segment, bar)
                            )
                        )
                    tmp_list.dump(f'{self.cache_dir}/filelist.m3u8')
                    await asyncio.gather(*tasks)
            else:
                click.echo('Live streaming media is not suppported!')
