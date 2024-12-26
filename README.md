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

## Some Useful Suggestions
If you are using an Intel laptop without a dedicated graphics card (i.e., ThinkPad T14 Gen2 w/ NVIDIA MX450) or you have to use Intel CPU to encode videos:  
Please apply the patch below:  
```
diff --git a/video_clipper/app.py b/video_clipper/app.py
index 8cfce8a..42b96fd 100644
--- a/video_clipper/app.py
+++ b/video_clipper/app.py
@@ -14,7 +14,7 @@ import yaml
 BASE_DIR = pathlib.Path(__file__).resolve().parent
 SAMPLE_MANIFEST = BASE_DIR / 'data' / 'manifest.sample.yaml'
 
-DEFAULT_VIDEO_CODEC = 'libx264'
+DEFAULT_VIDEO_CODEC = 'h264_qsv'
 if platform.system() == 'Darwin':
     DEFAULT_VIDEO_CODEC = 'h264_videotoolbox'
```

The `h264_qsv` encoder uses Intel's QuickSync, and has about 2x better performance than `libx264` in pure CPU scenarios.

## License
GPLv3
