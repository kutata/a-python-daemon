#!/usr/bin/env python
import sys
from time import sleep
from subprocess import Popen
from os import listdir
from os.path import getmtime, isfile, join
import re

command = 'python'
if len(sys.argv) < 2:
  exit('Please specified watch file.')

watch_file = sys.argv[1]

# get files and files mtime
SUFFIX_IGNORE = ['.jpg', '.png', '.gif', '.pyc', '.log', '.pk']
FILES_IGNORE = []
FOLDERS_IGNORE = ['.git']

SUFFIX_IGNORE_PATTERN = '|'.join(str(x) for x in SUFFIX_IGNORE) + '|^\..+'

def get_files(path):
  fs = listdir(path)
  files = []
  for f in fs:
    if not isfile(join(path, f)):
      # folder pttern here
      if f in FOLDERS_IGNORE:
        continue

      files += get_files(join(path, f))
    else:
      if f in FILES_IGNORE:
        continue
      if re.search(SUFFIX_IGNORE_PATTERN, f):
        continue

      files.append(join(path, f))

  return files

def get_mtime(files):
  return [(f, getmtime(f)) for f in files]

# run the specified script with subprocess
def start():
  p = Popen([command, watch_file]);
  return p

try:
  FILES = get_files('./')
  FILES_MTIMES = get_mtime(FILES)
  p = start()

  while True:
    for f, mtime in FILES_MTIMES:
      if (isfile(f)):
        if getmtime(f) != mtime:
          print('\nfile: ' + f + ' has changed.')
          print('--------- restarted --------\n')

          if not p is None:
            p.kill()

            FILES = get_files('./')
            FILES_MTIMES = get_mtime(FILES)

            p = start()

    sleep(1)

except KeyboardInterrupt:
  p.kill()
  print('\n Stopped')
