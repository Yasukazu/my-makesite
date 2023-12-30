import sys

YAT_IMPORT = "from yattag import Doc"

with open(sys.argv[1], 'r') as fi:
  cur_ind = 0
  for line in fi:
    def get_ind():
      return len(line) - len(line.rstrip())
    pass
