# -*- coding: utf-8 -*-
import typing as ty # noqa: F401

import pathlib
import platform

BASE_DIR = pathlib.Path(__file__).resolve().parent
MANIFEST_TEMPLATE = BASE_DIR / 'templates' / 'manifest.template.yaml'

GENERIC_VIDEO_CODECS = [
    'libx264',
    'libx265'
]

DEFAULT_VIDEO_CODEC = 'h264_nvenc'
if platform.system() == 'Darwin':
    DEFAULT_VIDEO_CODEC = 'h264_videotoolbox'


SOURCE_VIDEO_PLACEHOLDER = 'path/to/source/video.mp4'
OUTPUT_DIRECTORY_PLACEHOLDER = 'path/to/output/directory'
CLIP1_START_PLACEHOLDER = '00:00:00.000'
CLIP1_END_PLACEHOLDER = '01:23:45.678'
CLIP1_TITLE_PLACEHOLDER = 'Title of the Clip 1'
