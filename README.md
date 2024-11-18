# MP4 Compress

## Requirements

- Python 3.8
- FFmpeg

## Installation

Install `ffmpeg-python`.

```sh
pip install ffmpeg-python
```

Change the input file name, output file name, and output size (in KB) in `main.py`.

```py
compress_video('input.mp4', 'output.mp4', 5 * 1000)
```

Run.

```sh
python main.py
```
