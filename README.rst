#########
hls-get
#########

An asynchronous terminal-based hls video stream (m3u8) downloader & combiner, with AES-128 decryption support.


License: GNU General Public License v3

--------
Usage
--------

hls-get [OPTIONS] [LINKS]...

  Download m3u8 links (like "http://www.example.domain/path/to/index.m3u8#Save name" etc.) asynchronously, and merge into mp4 files.

Options:
  -P, --path TEXT      Save path
  -N, --names TEXT     Save name
  -C, --coros INTEGER  Max coroutines
  -H, --headers TEXT   Headers parameters just like curl's
  --help               Show this message and exit.

