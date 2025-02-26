# -*- coding: utf-8 -*-
from __future__ import annotations

import typing as ty  # noqa: F401

import unittest
from functools import partial

from .constants import TEST_FFMPEG_PROGRESS_OUTPUT


def assert_type_of(type_, obj, case_, *args, **kwargs):
    case_.assertIsInstance(obj, type_)

def check_progress(progress: str, case_, *args, **kwargs):
    case_.assertIn(progress, case_.PROGRESS_ACCEPTABLE_VALUES)


class TestExtractProgress(unittest.TestCase):

    PROGRESS_ACCEPTABLE_VALUES = {
        "continue",
        "end"
    }

    PROGRESS_FIELDS = {
        'total_size': partial(assert_type_of, int),
        'out_time_us': partial(assert_type_of, int),
        'out_time_ms': partial(assert_type_of, int),
        'out_time': partial(assert_type_of, str),
        'dup_frames': partial(assert_type_of, int),
        'drop_frames': partial(assert_type_of, int),
        'speed': partial(assert_type_of, str),
        'progress': check_progress
    }

    def test_extract_ffmpeg_progress(self):
        from video_clipper.ffmpeg_wrapper import extract_ffmpeg_progress

        in_ = TEST_FFMPEG_PROGRESS_OUTPUT.read_text()
        out_ = extract_ffmpeg_progress(in_)

        self.assertEqual(len(out_), 2)

        for progress in out_:
            for k, validator in self.PROGRESS_FIELDS.items():
                v = progress[k]
                validator(v, self)
