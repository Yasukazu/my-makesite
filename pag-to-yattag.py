# convert Pag to Yat-tag Python
import sys
import re

YAT_IMPORT = \
"""from yattag import Doc"
doc,tag,text,line = Doc.ttl()
"""

line = ''
def trim_indent() -> int:
  indent = 0
  for ind, c in enumerate(line):
    if not c in {' ', '\t'}:
      break
    indent += 1 if c == ' ' else 2
  line = line[ind:]
  return indent

def trim_text() -> bool:
  match = re.search(r'^\s*|\s+', line)
  if match:
    spcs = match[0]
    line = line[len(spcs):]
    return True
  return False

def trim_tag() -> str:
  def trim_attr() -> str:

    if not line.find(')'):
      raise ValueError("No closing paren.!")
    pass
  match = re.search(r'^\s*(\w+)([\(\s\t])', line)
  if not match:
    return None
  tag = match[1]
  with_attr = match[2] == '('
  if not with_attr:
    return tag
  line = line[match[0]+1:].rstrip()
  attr = trim_attr()
  if after_tag[0] == '(':
    if not after_tag.find(')'):
      raise ValueError("No closing paren.!")
  line = line[len(spcs):]
  for ind, c in enumerate(line):
    if not (c.isalpha() or c == '|'): break
  if '|' in line[:ind] and ind > 1:
    raise ValueError("Illegal '|'!")
  tag = line[:ind] # if ind == len(line) - 1: return line
  line = line[ind:]

  return tag

def trim_paren() -> str:
  p_open = line.find('(')
  if p_open >= 0:
    pass


tag = ''
indent = ''
with_on = False
with open(sys.argv[1], 'r') as fi:
  cur_ind = ''
  for line in fi:
    org_line = line
    line = line.strip('\n')
    if not line: continue
    output = []
    old_indent = indent
    pass
  match = re.search(r'^\s*(\w+)([\(\s\t])', line)
  if not match:
    return None
  tag = match[1]
  with_attr = match[2] == '('
  if not with_attr:
    return tag
  line = line[match[0]:].rstrip()
  attr = trim_attr()
  if after_tag[0] == '(':
    if not after_tag.find(')'):
      raise ValueError("No closing paren.!")
  line = line[len(spcs):]
  for ind, c in enumerate(line):
    if not (c.isalpha() or c == '|'): break
  if '|' in line[:ind] and ind > 1:
    raise ValueError("Illegal '|'!")
  tag = line[:ind] # if ind == len(line) - 1: return line
  line = line[ind:]

  return tag

def trim_paren() -> str:
  p_open = line.find('(')
  if p_open >= 0:
    pass


tag = ''
indent = ''
with_on = False
with open(sys.argv[1], 'r') as fi:
  cur_ind = ''
  for line in fi:
    org_line = line
    line = line.strip('\n')
    if not line: continue
    output = []
    old_indent = indent
    indent = trim_indent()
    output.append(indent)
    is_text = trim_text()
    if is_text:
      print(''.join(output + ['text(', line, ')']))
      continue

    tag = trim_tag()
    output.append(tag)
    with_on = len(indent) > len(old_indent)
    if with_on:
        output.append('with ')
    
        output_list += [new_ind, 'with ']
        if rs_line[0] == '|':
           output_list.append('text(')
        
        cur_ind = new_ind
