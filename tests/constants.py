# -*- coding: utf-8 -*-
import pathlib

TEST_BASE_DIR = pathlib.Path(__file__).resolve().parent
TEST_DATA_DIR = TEST_BASE_DIR / 'testdata'

TEST_FFMPEG_PROGRESS_OUTPUT = TEST_DATA_DIR / 'ffmpeg_progress.log'
