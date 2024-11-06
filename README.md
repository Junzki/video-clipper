# video-clipper

Clips multiple video clips from one video file.

## Usage

1. Install  
   ```pip install video-clipper-r```
2. Create `manifest.yaml` with command below:  
   ```python -m video_clipper init-manifest```
3. Run `python -m videp_clipper manifest.yaml` to start clipping.

## Why the Package Has a Different Name?
PyPI told me the original name `video-clipper` was similiar to some existing package(s), so I renamed release package - added a `r` as suffix.  
The suffix `r` means nothing. Sometimes we add `r` or `R` after a software name to show this is totally a different software.

## Requirements
1. Python 3.8+
2. FFmpeg  
   (Please add FFmpeg to your PATH environment variable)

## License
GPLv3
