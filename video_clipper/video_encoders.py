# -*- coding: utf-8 -*-
from __future__ import annotations

import typing as ty  # noqa: F401

import platform
from .ffmpeg_wrapper import FFmpegCmd


def list_hardware_accel_devices() -> ty.List[str]:
    cmd = FFmpegCmd(['-hide-banner', '-hwaccels'])
    out = cmd.execute()
    raw_ = out.stdout.decode().split('\n')
    hwaccels = [x.strip() for x in raw_[1:] if x.strip()]
    return hwaccels


def support_nvenc(codec_list: ty.List[str]) -> bool:
    return 'nvenc' in codec_list


def get_available_video_codecs() -> ty.List[str]:
    return [
        'h264_nvenc',
        'h264_videotoolbox',
        'libx264',
        'libx265',
        'libvpx-vp9'
    ]


def check_nvenc_available() -> bool:
    return 'nvenc' in get_available_video_codecs()


def get_default_video_codec() -> str:
    DEFAULT_VIDEO_CODEC = 'h264_nvenc'
    if platform.system() == 'Darwin':
        DEFAULT_VIDEO_CODEC = 'h264_videotoolbox'
    return DEFAULT_VIDEO_CODEC