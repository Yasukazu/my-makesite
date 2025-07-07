# pykakasi test
import pykakasi
from pykakasi import kakasi, wakati

def conv_do(text: str, conv_func_i='K'):
    conv_func = kakasi() if conv_func_i[0].lower() == 'k' else wakati()
    conv_func.setMode("H","a") # Hiragana to ascii, default: no conversion
    conv_func.setMode("K","a") # Katakana to ascii, default: no conversion
    conv_func.setMode("J","a") # Japanese to ascii, default: no conversion
    conv_func.setMode("r","Hepburn") # default: use Hepburn Roman table
    #kakasi.setMode("s", True) # add space, default: no separator
    #kakasi.setMode("C", True) # capitalize, default: no capitalize
    convtr = conv_func.getConverter()
    result = convtr.do(text)
    return(result)

from sys import argv

def test_attrs(text: str):
    kks = pykakasi.kakasi()
    result = kks.convert(text)
    for it in result:
        print(f"it[orig]:{it['orig']}, it[kana]:{it['kana']}, it[hira]:{it['hira']}, it['hepburn']:{it['hepburn']}, kunrei: {it['kunrei']}")
if __name__ == '__main__':
    from sys import argv
    text = argv[1] #"かな漢字"
    print(test_attrs(text)) # conv_do(text, argv[1]))