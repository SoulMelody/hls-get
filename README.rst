#########
hls-get
#########

An asynchronous terminal-based hls(HTTP Live Streaming) VoD video stream (m3u8) downloader & simple combiner, with AES-128 decryption support.


License: GNU General Public License v3

--------
Usage
--------

hls-get [OPTIONS] [LINKS]...

  Download m3u8 links (like "http://www.example.domain/path/to/index.m3u8#Save name" etc.) asynchronously, and merge into mp4 files.

Options:
  -P, --path TEXT            Save path
  -N, --names TEXT           Save name
  -C, --coros INTEGER        Max coroutines
  -H, --headers TEXT         Headers parameters like curl's
  -c, --clean-up             Clean up the cache directory when completed
  -D, --delay INTEGER        delay seconds before retrying
  -R, --retry-times INTEGER  Max retry times

