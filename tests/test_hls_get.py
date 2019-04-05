#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `hls_get` package."""

import aiohttp
import pytest
import uvloop
from click.testing import CliRunner

from hls_get import cli


@pytest.yield_fixture()
def event_loop():
    loop = uvloop.new_event_loop()
    yield loop
    loop.close()


@pytest.mark.asyncio
async def test_get_content(event_loop):
    async with aiohttp.ClientSession() as session:
        url = 'http://httpbin.org/get'
        async with session.get(url) as resp:
            content = await resp.read()
            assert resp.status == 200


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert 'Show this message and exit.' in help_result.output
