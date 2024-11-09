# video-clipper

![PyPI v0.2.2](https://img.shields.io/pypi/v/video-clipper-r)

Clips multiple video clips from one video file.

## Usage

1. Install  
   ```bash
   pip install video-clipper-r
   ```
2. Create `manifest.yaml` with command below:  
   ```bash
   python -m video_clipper init-manifest  --source-video "path/to/source/video.mp4"
   ```
   This command will create a `manifest.yaml` file in the same directory with the preferred source video.   

3. Run command below to start clipping.
   ```bash
   python -m video_clipper clip manifest.yaml
   ```

## Why the Package Has a Different Name?
The PyPI told me the original name `video-clipper` was similiar to some existing package(s), so I renamed release package to `video-clipper-r` - added an "r" as suffix.  
The suffix "r" means nothing. Sometimes we add "r" or "R" after a software name to show this is totally a different software.

## Requirements
1. Python 3.8+
2. FFmpeg  
   (Please add FFmpeg to your PATH environment variable)

## License
GPLv3
