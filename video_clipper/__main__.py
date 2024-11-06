# -*- coding: utf-8 -*-
import typing as ty  # noqa: F401

import argparse
from .app import Manifest, VideoClipper, create_manifest

CMD_INIT_MANIFEST = 'init-manifest'

parser = argparse.ArgumentParser()
parser.add_argument('--target-dir', type=str,
                    help='Target directory to create manifest file or output clips.')
parser.add_argument('manifest', type=str)


def main():
    args, _ = parser.parse_known_args()

    target_dir_ = args.target_dir

    if CMD_INIT_MANIFEST == args.manifest:
        create_manifest(target_dir_)
        exit(0)
    else:
        manifest_ = Manifest.parse_manifest(args.manifest)

    clipper = VideoClipper()
    clipper.clip_from_manifest(manifest_)


if __name__ == '__main__':
    main()
