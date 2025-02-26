# -*- coding: utf-8 -*-
from __future__ import annotations

import os
import typing as ty  # noqa: F401
import dataclasses
import yaml
from jinja2.filters import do_mark_safe

from video_clipper.constants import DEFAULT_OUTPUT_EXTENSION


@dataclasses.dataclass
class VideoClip:
    start: str
    end: str
    title: ty.Union[str, None] = None
    output_filename: ty.Union[str, None] = None
    compress_output: bool = True

    def __str__(self):
        return f"ClipTask(start={self.start}, end={self.end}, title={self.title})"

    def __repr__(self):
        return self.__str__()


@dataclasses.dataclass
class ClipBatch:
    source: str
    output_dir: str

    clips: ty.List[VideoClip] = dataclasses.field(default_factory=list)
    output_extension: str = DEFAULT_OUTPUT_EXTENSION
    compress_output: bool = True

def parse_manifest(input_file_: str) -> ty.List[ClipBatch]:
    with open(input_file_, 'r') as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)

    source = data['source']
    output_dir = data.get('output_dir', None)
    output_ext = data.get('output_extension', DEFAULT_OUTPUT_EXTENSION)
    compress_output = data.get('compress_output', 'yes').lower() == 'yes'

    if not os.path.isdir(source):
        files = [(source, data['clips'])]
    else:
        files = list()
        for f_ in data['files']:
            name_ = f_['filename']
            name_ = os.path.join(source, name_)
            clips_ = f_['clips']
            files.append((name_, clips_))

    tasks = list()

    for source_, clips_ in files:
        out_ = ClipBatch(source_, output_dir,
                         output_extension=output_ext,
                         compress_output=compress_output)

        for clip in clips_:
            start = clip['start']
            end = clip['end']
            title = clip.get('title', None)
            out_.clips.append(VideoClip(start, end, title,
                                        compress_output=compress_output))

        tasks.append(out_)

    return tasks
