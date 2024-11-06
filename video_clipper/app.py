# -*- coding: utf-8 -*-
from __future__ import annotations

import shutil
import typing as ty  # noqa: F401

import os
import platform
import pathlib
import dataclasses
import subprocess
import yaml

BASE_DIR = pathlib.Path(__file__).resolve().parent
SAMPLE_MANIFEST = BASE_DIR / 'data' / 'manifest.sample.yaml'

DEFAULT_VIDEO_CODEC = 'libx264'
if platform.system() == 'Darwin':
    DEFAULT_VIDEO_CODEC = 'h264_videotoolbox'


@dataclasses.dataclass
class VideoClip:
    start: str
    end: str
    title: ty.Union[str, None] = None
    output_filename: ty.Union[str, None] = None


@dataclasses.dataclass
class Manifest:
    source: str
    output_dir: ty.Union[str, None] = None
    clips: ty.List[VideoClip] = dataclasses.field(default_factory=list)
    output_extension: str | None = None

    @classmethod
    def parse_manifest(cls, input_file_: str):
        with open(input_file_, 'r') as f:
            data = yaml.load(f, Loader=yaml.SafeLoader)

        source = data['source']
        output_dir = data.get('output_dir', None)
        output_ext = data.get('output_extension')

        if not output_dir:
            output_dir = os.path.join(os.path.dirname(source), 'clips')

        out_ = cls(source, output_dir, output_extension=output_ext)

        for clip in data['clips']:
            start = clip['start']
            end = clip['end']
            title = clip.get('title', None)
            out_.clips.append(VideoClip(start, end, title))

        return out_


class VideoClipper(object):

    DEFAULT_OUTPUT_EXT = 'mp4'
    DEFAULT_OUTPUT_VIDEO_CODEC = ['-codec:v', DEFAULT_VIDEO_CODEC, '-vf', 'scale=1920:1080', '-b:v', '6000k']
    DEFAULT_OUTPUT_AUDIO_CODEC = ['-codec:a', 'aac']
    CLIPPING_CODEC = ['-c', 'copy']

    class _Context(object):

        def __init__(self):
            self.initial_params = ['ffmpeg', ]
            self.input_params = list()
            self.output_params = list()

        def execute(self):
            cmd = [
                *self.initial_params,
                *self.input_params,
                *self.output_params
            ]

            print("Cmd: ", subprocess.list2cmdline(cmd))
            subprocess.run(cmd)

    @staticmethod
    def initial_ffmpeg(ctx: _Context) -> _Context:
        ctx.initial_params.extend([
            '-hide_banner'
        ])
        return ctx

    @staticmethod
    def build_input(ctx: _Context, m: Manifest) -> _Context:
        ctx.input_params.extend(['-i', m.source])
        return ctx

    def build_default_clip_name(self, source: str, start: str, end: str) -> str:
        _, source_name = os.path.split(source)
        name, ext = os.path.splitext(source_name)
        return f'clip_{name}_{start}_{end}.{self.DEFAULT_OUTPUT_EXT}'


    def build_output(self, ctx: _Context,
                     manifest: Manifest, clip: VideoClip) -> (_Context, VideoClip):
        if not clip.title:
            clip_name = self.build_default_clip_name(manifest.source, clip.start, clip.end)
        else:
            clip_name = f'{clip.title}.{self.DEFAULT_OUTPUT_EXT}'

        if manifest.output_dir:
            clip_name = os.path.join(manifest.output_dir, clip_name)

        clip.output_filename = clip_name

        ctx.output_params.extend(['-ss', str(clip.start), '-to', str(clip.end),
                                  *self.CLIPPING_CODEC,
                                  '-y', clip_name])
        return ctx, clip

    def compress_clip(self, c: VideoClip) -> None:
        ctx = self._Context()
        ctx = self.initial_ffmpeg(ctx)

        source = c.output_filename
        name, ext = os.path.splitext(source)
        dest = f'{name}_compressed{ext}'

        ctx.input_params.extend(['-i', c.output_filename])
        ctx.output_params.extend([*self.DEFAULT_OUTPUT_VIDEO_CODEC, *self.DEFAULT_OUTPUT_AUDIO_CODEC,
                                  '-y', dest])

        ctx.execute()

        os.remove(source)

    def clip_from_manifest(self, manifest: Manifest,
                           target_dir: str = None) -> None:
        if not os.path.exists(manifest.output_dir):
            os.makedirs(manifest.output_dir, exist_ok=True)

        if not os.path.exists(manifest.source):
            raise FileNotFoundError(f"Source file {manifest.source} does not exist.")

        ctx = self._Context()
        ctx = self.initial_ffmpeg(ctx)
        ctx = self.build_input(ctx, manifest)

        proceed_clips = list()

        for clip in manifest.clips:
            ctx, clip = self.build_output(ctx, manifest, clip)
            proceed_clips.append(clip)

        ctx.execute()

        for clip in proceed_clips:
            self.compress_clip(clip)


def create_manifest(target: ty.Optional[str] = None):
    if not target:
        target = os.path.join(os.getcwd(), 'manifest.yaml')
    elif os.path.isdir(target):
        target = os.path.join(target, 'manifest.yaml')

    shutil.copy(SAMPLE_MANIFEST, target)
    print(target)
