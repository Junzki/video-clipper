# -*- coding: utf-8 -*-
import typing as ty # noqa: F401

import os
import subprocess
import time

import jinja2
import click

from .constants import MANIFEST_TEMPLATE, COMMON_VIDEO_FILE_EXTENSIONS
from .constants import SOURCE_VIDEO_PLACEHOLDER, OUTPUT_DIRECTORY_PLACEHOLDER
from .constants import CLIP1_START_PLACEHOLDER, CLIP1_END_PLACEHOLDER, CLIP1_TITLE_PLACEHOLDER


def probe_duration(source_video: str) -> str:
    """
    Get the duration via ffprobe from input media file
    in case ffmpeg was run with loglevel=error.

    :param source_video: Path to the source video file.
    :return: Duration of the video in HH:MM:SS.ffffff format.
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


# def _build_manifest(source_video: str,
#                     output_dir: str) -> (ty.Dict[str, ty.Any], str):
#     clip_1_start = CLIP1_START_PLACEHOLDER
#     clip_1_end = CLIP1_END_PLACEHOLDER
#     clip_1_title = CLIP1_TITLE_PLACEHOLDER
#
#     default_target = None
#
#     if source_video:
#         source_video = os.path.abspath(source_video)
#         if not os.path.exists(source_video):
#             raise FileNotFoundError(f"File not found: {source_video}")
#
#         clip_1_end = probe_duration(source_video)
#         _, clip_1_title = os.path.split(source_video)
#
#         default_target = os.path.dirname(source_video)
#
#
#     if output_dir:
#         if os.path.exists(output_dir):
#             if not os.path.isdir(output_dir):
#                 raise NotADirectoryError(f"Path exists but is not a directory: {output_dir}")
#
#             output_dir = os.path.abspath(output_dir)
#         else:
#             os.makedirs(output_dir, exist_ok=True)
#             output_dir = os.path.abspath(output_dir)
#     elif source_video:
#         output_dir = os.path.join(os.path.dirname(source_video), 'clips')
#         os.makedirs(output_dir, exist_ok=True)
#         output_dir = os.path.abspath(output_dir)
#
#     context = dict(source_video=source_video or SOURCE_VIDEO_PLACEHOLDER,
#                    output_dir=output_dir or OUTPUT_DIRECTORY_PLACEHOLDER,
#                    clip_1_start=clip_1_start,
#                    clip_1_end=clip_1_end,
#                    clip_1_title=clip_1_title)
#
#     return context, default_target


def scan_video_files(directory: str) -> ty.List[str]:
    """
    Scan a directory for video files.

    :param directory: Path to the directory to scan.
    :return: List of video files found in the directory.
    """

    files = os.listdir(directory)
    video_files = list()

    for f in files:
        _, ext = os.path.splitext(f)
        if ext[1:].lower() in COMMON_VIDEO_FILE_EXTENSIONS:
            video_files.append(f)

    return video_files


def create_output_dir_by_source(source: str, source_is_dir: bool = False) -> str:
    if not source_is_dir:
        source = os.path.dirname(source)

    output_dir = os.path.join(source, 'clips')
    return output_dir


def create_target_by_source(source: str, source_is_dir: bool = False) -> str:
    if not source_is_dir:
        source = os.path.dirname(source)

    target = os.path.join(source, 'manifest.yaml')
    return target


def create_manifest(target: ty.Optional[str] = None,
                    source: ty.Optional[str] = None,
                    output_dir: ty.Optional[str] = None,
                    overwrite_manifest: bool = True) -> None:
    source_is_dir = False
    if os.path.isdir(source):
        source_is_dir = True
        video_files = scan_video_files(source)
    elif os.path.exists(source):
        video_files = [source, ]
    else:
        raise FileExistsError("File not found: %s" % source)

    context = dict(source=source,
                   source_is_dir=source_is_dir,
                   output_dir=output_dir or create_output_dir_by_source(source, source_is_dir),
                   files=list(),
                   clips=list())

    for video_file in video_files:
        if source_is_dir:
            file_path_ = os.path.join(source, video_file)
            clip_1_title = video_file
        else:
            file_path_ = video_file
            _, clip_1_title = os.path.split(file_path_)

        print("Found: %s" % file_path_)

        clip_1_start = CLIP1_START_PLACEHOLDER
        clip_1_end = probe_duration(file_path_)

        context['files'].append(dict(filename=video_file,
                                     clips=[dict(start=clip_1_start,
                                                 end=clip_1_end,
                                                 title=clip_1_title)]))

    if not source_is_dir:
        context['clips'] = context['files'][0]['clips']

    with open(MANIFEST_TEMPLATE, 'r') as f:
        template = jinja2.Template(f.read())

    rendered = template.render(**context)

    target = target or create_target_by_source(source, source_is_dir)
    if os.path.isdir(target):
        target = os.path.join(target, 'manifest.yaml')
    elif os.path.exists(target) and not overwrite_manifest:
        raise FileExistsError("File already exists: %s" % target)

    with open(target, 'w') as f:
        f.write(rendered)

    print(target)


@click.command(name='init-manifest')
@click.option( '--target', type=click.Path(dir_okay=True),
              help='Path to the manifest file to be created.')
@click.option( '--overwrite-manifest', type=click.BOOL, default=True,
              help='Path to the source video file or directory.')
@click.option( '--source', type=click.Path(exists=True, dir_okay=True),
               help='Path to the source video file.')
@click.option( '--output-dir', type=click.Path(file_okay=False),
                help='Path to the output directory.')
def cli_init_manifest(target: ty.Optional[str] = None,
                      source: ty.Optional[str] = None,
                      output_dir: ty.Optional[str] = None,
                      overwrite_manifest: bool = True) -> None:
    return create_manifest(target, source, output_dir, overwrite_manifest)
