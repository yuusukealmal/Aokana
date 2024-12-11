import struct, json
from dataclasses import dataclass

@dataclass
class fe:
    p: int
    L: int
    k: int

ti = {}
def ToInt32(arr, index):
    return struct.unpack('<i', arr[index:index+4])[0]

def ToUint32(arr, index):
    return struct.unpack('<I', arr[index:index+4])[0]

def init(fp):
    f = open(fp, 'rb')

    array = bytearray(f.read(1024))

    num = 0
    for i in range(4, 255):
        num += ToInt32(array, i*4)
    
    array2 = bytearray(f.read(16 * num))
    dd(array2, len(array2),ToUint32(array, 212))
    
    num2 = ToInt32(array2, 12)
    num3 = num2 - (1024 + len(array2))
    array3 = bytearray(f.read(num3))
    dd(array3, num3, ToUint32(array, 92))

    init2(array2, array3, num)

def init2(rtoc, rpaths, numfiles):
    num = 0
    for i in range(numfiles):
        num2 = 16 * i
        l = ToUint32(rtoc, num2)
        num3 = ToInt32(rtoc, num2+4)
        k = ToUint32(rtoc, num2+8)
        p = ToUint32(rtoc, num2+12)
        for j in range(num3, len(rpaths)):
            if rpaths[j] == 0:
                break
        key = rpaths[num:j].decode('ascii').lower()
        value = str(fe(p, l, k))
        ti[key] = value
        num = j + 1

def dd(b, L, k):
    array = bytearray(256)
    gk(array, k)
    for i in range(L):
        b2 = b[i]
        b2 ^= array[i % 253]
        b2 = (b2 + 3) & 0xFF
        b2 = (b2 + array[i % 89]) & 0xFF
        b2 ^= 153
        b[i] = b2 & 0xFF

def gk(b, k0):
    num = k0*7391+42828
    num2 = (num<<17)^num
    for i in range(256):
        num = (num - k0 + num2) & 0xFFFFFFFF
        num2 = (num + 56) & 0xFFFFFFFF
        num = (num * (num2 & 239)) & 0xFFFFFFFF
        b[i] = num & 0xFF
        num >>= 1

def Data(fn):
    if fn in ti:
        return ti[fn]
    return None

init('./aokana_data/bg.dat')
with open('ti.json', 'w') as f:
    json.dump(ti, f)
print(ti)