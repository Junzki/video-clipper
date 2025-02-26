# -*- coding: utf-8 -*-
from __future__ import annotations

import typing as ty  # noqa: F401

import platform
from .ffmpeg_wrapper import FFmpegCmd


class VideoEncoderProvider(object):

    @staticmethod
    def list_hardware_accel_devices() -> ty.List[str]:
        cmd = FFmpegCmd(['-hide-banner', '-hwaccels'])
        out = cmd.execute()
        raw_ = out.stdout.decode().split('\n')
        hwaccels = [x.strip() for x in raw_[1:] if x.strip()]
        return hwaccels

    def get_codec_list(self) -> ty.List[str]:
        """ List prioritized codecs based on hardware acceleration availability.
        """
        codecs = [
            'libx264',
            'libx265'
        ]

        if platform.system() == 'Darwin':
            codecs.append('h264_videotoolbox')

        accel_devices = self.list_hardware_accel_devices()
        if 'vaapi' in accel_devices:
            codecs.append('h264_vaapi')

        if 'cuda' in accel_devices:
            codecs.append('h264_nvenc')

        codecs.reverse()

        return codecs

    def __init__(self):
        self._codec_list = self._get_codec_list()
    ...





def support_nvenc(codec_list: ty.List[str]) -> bool:
    return 'cuda' in codec_list

def support_vaapi(codec_list: ty.List[str]) -> bool:
    return 'vaapi' in codec_list


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