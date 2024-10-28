# video-clipper

Clips multiple video clips from one video file.

## Usage

1. Copy `manifest.sample.yaml`, rename it to `manifest.yaml` and fill in the details.
2. Run `python app.py manifest.yaml` to start clipping.

## Requirements
1. Python 3.8+
2. FFmpeg
3. PyYAML

## Note for non-macOS users
Please change the video codec in `app.py` to `libx264` or any other codec that is supported by your FFmpeg installation.

## License
GPLv3
