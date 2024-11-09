# -*- coding: utf-8 -*-
import typing as ty # noqa: F401

import os
import subprocess
import time

import jinja2
import click

from .constants import MANIFEST_TEMPLATE
from .constants import SOURCE_VIDEO_PLACEHOLDER, OUTPUT_DIRECTORY_PLACEHOLDER
from .constants import CLIP1_START_PLACEHOLDER, CLIP1_END_PLACEHOLDER, CLIP1_TITLE_PLACEHOLDER


def probe_duration(source_video: str) -> str:
    """
    Get the duration via ffprobe from input media file
    in case ffmpeg was run with loglevel=error.

    Args:
        cmd (List[str]): A list of command line elements, e.g. ["ffmpeg", "-i", ...]

    Returns:
        Optional[int]: The duration in milliseconds.
    """

    output = subprocess.check_output(
        [
            "ffprobe",
            "-loglevel", "error",
            "-hide_banner",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            source_video,
        ],
        universal_newlines=True,
    )

    output = output.strip()
    duration, duration_milli = output.split('.')

    duration_formatted = time.strftime("%H:%M:%S", time.gmtime(int(duration)))
    return f"{duration_formatted}.{duration_milli}"


def _build_manifest(source_video: str,
                    output_dir: str) -> (ty.Dict[str, ty.Any], str):
    clip_1_start = CLIP1_START_PLACEHOLDER
    clip_1_end = CLIP1_END_PLACEHOLDER
    clip_1_title = CLIP1_TITLE_PLACEHOLDER

    default_target = None

    if source_video:
        source_video = os.path.abspath(source_video)
        if not os.path.exists(source_video):
            raise FileNotFoundError(f"File not found: {source_video}")

        clip_1_end = probe_duration(source_video)
        _, clip_1_title = os.path.split(source_video)

        default_target = os.path.dirname(source_video)


    if output_dir:
        if os.path.exists(output_dir):
            if not os.path.isdir(output_dir):
                raise NotADirectoryError(f"Path exists but is not a directory: {output_dir}")

            output_dir = os.path.abspath(output_dir)
        else:
            os.makedirs(output_dir, exist_ok=True)
            output_dir = os.path.abspath(output_dir)
    elif source_video:
        output_dir = os.path.join(os.path.dirname(source_video), 'clips')
        os.makedirs(output_dir, exist_ok=True)
        output_dir = os.path.abspath(output_dir)

    context = dict(source_video=source_video or SOURCE_VIDEO_PLACEHOLDER,
                   output_dir=output_dir or OUTPUT_DIRECTORY_PLACEHOLDER,
                   clip_1_start=clip_1_start,
                   clip_1_end=clip_1_end,
                   clip_1_title=clip_1_title)

    return context, default_target


def create_manifest(target: ty.Optional[str] = None,
                    source_video: ty.Optional[str] = None,
                    output_dir: ty.Optional[str] = None):
    context, default_target = _build_manifest(source_video, output_dir)

    with open(MANIFEST_TEMPLATE, 'r') as f:
        template = jinja2.Template(f.read())

    rendered = template.render(**context)

    target = target or default_target
    if not target:
        target = os.getcwd()

    if os.path.exists(target):
        if os.path.isdir(target):
            target = os.path.join(target, 'manifest.yaml')
        else:
            raise FileExistsError(f"File already exists: {target}")
    else:
        os.makedirs(target, exist_ok=True)
        target = os.path.join(target, 'manifest.yaml')

    with open(target, 'w') as f:
        f.write(rendered)

    print(target)


@click.command(name='init-manifest')
@click.option( '--target', type=click.Path(dir_okay=True),
              help='Path to the manifest file to be created.')
@click.option( '--source-video', type=click.Path(exists=True, dir_okay=False),
               help='Path to the source video file.')
@click.option( '--output-dir', type=click.Path(file_okay=False),
                help='Path to the output directory.')
def cli_init_manifest(target: ty.Optional[str] = None,
                      source_video: ty.Optional[str] = None,
                      output_dir: ty.Optional[str] = None):
    return create_manifest(target, source_video, output_dir)
