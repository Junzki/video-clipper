# -*- coding: utf-8 -*-
from __future__ import annotations

import typing as ty  # noqa: F401

import re
import sys
import subprocess

PROGRESS_PATTERN = re.compile(
    r"total_size=(\d+)\s+out_time_us=(\d+)\s+out_time_ms=(\d+)\s+out_time=([\d:.]+)\s+dup_frames=(\d+)\s+drop_frames=(\d+)\s+speed=([\d.e+-]+)\s+progress=(\w+)"
)

""" A progress should start from `total_size` and end with `progress` """
PROGRESS_BEGIN = "total_size="
PROGRESS_END = "progress="
PROGRESS_KEY_VALUE_SEP = "="


PROGRESS_FIELDS = {
    'total_size': int,
    'out_time_us': int,
    'out_time_ms': int,
    'out_time': str,
    'dup_frames': int,
    'drop_frames': int,
    'speed': str,
    'progress': str
}

DEFAULT_PROGRESS_FIELD_CLEAN = (lambda x: x)



def extract_ffmpeg_progress(in_: str) -> (bool, ty.Dict[str, ty.Any]):
    collected_progress = list()
    progress = dict()
    start_collect = False

    in_lines = in_.splitlines()
    for line in in_lines:
        line = line.strip()
        if not line:
            continue

        if line.startswith(PROGRESS_BEGIN):
            start_collect = True

        if line.startswith(PROGRESS_END):
            start_collect = False
            progress['progress'] = line.split(PROGRESS_KEY_VALUE_SEP, 1)[1]
            collected_progress.append(progress)
            progress = dict()

        if PROGRESS_KEY_VALUE_SEP not in line:
            continue

        if start_collect:
            k, v = line.split(PROGRESS_KEY_VALUE_SEP, 1)
            k = k.lower()
            v = v.strip()
            m = PROGRESS_FIELDS.get(k, DEFAULT_PROGRESS_FIELD_CLEAN)
            try:
                v = m(v)
            except Exception as e:
                print(f"Error parsing {k}: {e}", file=sys.stderr)

            progress[k] = v

    return collected_progress


class FFmpegCmd(object):

    def __init__(self, explicit_initial_params: ty.List[str] = None):
        if not explicit_initial_params:
            self.initial_params = [
                '-loglevel', 'quiet',  # Hide logs
                '-hide_banner',
            ]
        else:
            self.initial_params = explicit_initial_params
        self.input_params = list()
        self.output_params = list()

        self.video_length = 0

    def track_progress(self, final_time: int):
        self.video_length = final_time
        self.initial_params.extend(['-progress', 'pipe:2'])

    def execute(self):
        cmd = [
            'ffmpeg',
            *self.initial_params,
            *self.input_params,
            *self.output_params
        ]

        print("Cmd: ", subprocess.list2cmdline(cmd))

        out = subprocess.run(cmd, capture_output=True)
        return out
