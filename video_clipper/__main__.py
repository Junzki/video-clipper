# -*- coding: utf-8 -*-
import typing as ty  # noqa: F401

import click
from .clipper import cli_clip_with_manifest
from .init_manifest import cli_init_manifest

CMD_INIT_MANIFEST = 'init-manifest'


@click.group()
def cli():
    ...


cli.add_command(cli_init_manifest)
cli.add_command(cli_clip_with_manifest)


if __name__ == '__main__':
    cli()
