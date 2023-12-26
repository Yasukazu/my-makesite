import codecs
import sys

def all_ascii(s):
    return all(ord(c) < 128 for c in s)

f = open(sys.argv[1], 'r')
txt = f.read()
dcd = codecs.decode(txt, 'unicode-escape')
dlen = len(dcd)
cur = 0
tt = []
inout = []
stk = ''
inside = False
clog = [0]
while cur < dlen:
    pos = dcd[cur:].find('"')
    assert(pos != 0)
    if pos < 0:
        break
    if inside:
        # if pos + 1 > dlen: raise ValueError("No closing double quote!")
        stk = dcd[cur:cur + pos]
        if not all_ascii(stk):
            stk = stk.strip(" \n").rstrip(" \n")
        tt.append(stk)
        inout.append(True)
        inside = False
    else:
        tt.append(dcd[cur:cur + pos])
        inout.append(False)
        inside = True
    cur += pos + 1
    clog.append(cur)
        
if cur < dlen:
    tt.append(dcd[cur:])
    assert(not inside)
    inout.append(False)
    # raise ValueError("EOF in inside double quote!")
assert(len(tt) == len(inout))
output = []
for i,v in enumerate(tt):
    output.append(tt[i] if not inout[i] else f'"{tt[i]}"')
print(''.join(output))

