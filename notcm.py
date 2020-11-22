'''NotCloudMusic
又一个网易云音乐 CUI 客户端
https://github.com/NKID00/NotCloudMusic

MIT License

Copyright (c) 2020 NKID00

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.'''

from NeteaseCloudMusicApiPy.ncmapi import NeteaseCloudMusicApi
from sys import argv
from os import walk
from os.path import splitext
from importlib import import_module
from requests import ConnectionError, Timeout, HTTPError

USAGE = '''NotCloudMusic
又一个网易云音乐 CLI 客户端

usage: notcm <command> [<args>...]

commands:'''
USAGE_COMMAND = '  %-11s %s'

VERSION = 'NotCloudMusic 0.1.0'


def load_plugins():
    plugins = {}
    for file in next(walk('./plugins/'))[2]:
        name, ext = splitext(file)
        if ext == '.py':
            module = import_module(f'plugins.{name}')
            try:
                info = module.notcloudmusic_plugin_info
                plugins[info['name']] = info
            except AttributeError:
                continue
    commands = {}
    for name, plugin in plugins.items():
        try:
            commands.update(plugin['commands'])
        except AttributeError:
            continue
    return plugins, commands


def main():
    plugins, commands = load_plugins()
    if len(argv) < 2 or argv[1] not in commands.keys():
        print(USAGE)
        for name, command in sorted(commands.items()):
            print(USAGE_COMMAND % (name, command['description']))
    else:
        api = NeteaseCloudMusicApi()
        try:
            commands[argv[1]]['callable'](api, argv)
        except ConnectionError or Timeout or HTTPError:
            print('连接错误，请检查API进程是否启动且连接到互联网。')


if __name__ == "__main__":
    main()
