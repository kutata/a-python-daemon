#!/usr/bin/env python

import sys
from os import listdir, execv, execl, kill
from os.path import getmtime, isfile, join
import signal

import re
FILES_FILTER = '.jpg|.png|.gif|.pyc|.log|.pk|^\..+'
FOLDER_PATTERN = ''

command = 'python' # specified python version

def listmydir(path):
  fs = listdir(path)
  _fs = []
  for f in fs:
    if not isfile(join(path, f)):
      # folder pttern here
      _fs += listmydir(join(path, f))
    else:
      if re.search(FILES_FILTER, f) is None:
        _fs.append(join(path, f))

  return _fs

FILES = listmydir('./')

FILES_MTIMES = [(f, getmtime(f)) for f in FILES]

import time
from subprocess import Popen

p = None
pid = None

if len(sys.argv) > 2:
  pid = int(sys.argv[2])

try:
  if pid is not None:
    kill(pid, signal.SIGTERM)

  # p = Popen('./' + sys.argv[1], shell=True)
  p = Popen([command, sys.argv[1]])

except KeyboardInterrupt:
  print(KeyboardInterrupt)

try:
  while True:
    for f, mtime in FILES_MTIMES:
      if (isfile(f)):
        if getmtime(f) != mtime:
          print('file: ' + f + ' has changed.')
          print('--------- restarted --------')
          if p is None:
            execv(__file__, sys.argv)
          else:
            argv = sys.argv[:2] + [str(p.pid)]
            execv(__file__, argv)

    time.sleep(1)

except KeyboardInterrupt:
  p.kill()
  print('\nStopped')
