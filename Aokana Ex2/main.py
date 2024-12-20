import struct, json, os
from dataclasses import dataclass

@dataclass
class fe:
    p: int
    L: int
    k: int
    
    def todict(self):
        return {'p': self.p, 'L': self.L, 'k': self.k}

ti = {}
def ToInt32(arr, index):
    return struct.unpack('<i', arr[index:index+4])[0]

def ToUint32(arr, index):
    return struct.unpack('<I', arr[index:index+4])[0]

def init(fp):
    f = open(fp, 'rb')

    array = bytearray(f.read(1024))

    num = 0
    for i in range(3, 255):
        num = (num + ToInt32(array, i*4)) & 0xFFFFFFFF 
    
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
        num4 = num3
        while(num4<len(rpaths) and rpaths[num4] != 0):
            num4 += 1
        key = rpaths[num:num4].decode('ascii').lower()
        value = fe(p, l, k).todict()
        ti[key] = value
        num = num4 + 1

def dd(b, L, k):
    array = bytearray(256)
    gk(array, k)
    for i in range(L):
        b2 = b[i]
        b2 ^= array[i % 179]
        b2 = (b2 + 3) & 0xFF
        b2 = (b2 + array[i % 89]) & 0xFF
        b2 ^= 119
        b[i] = b2 & 0xFF

def gk(b, k0):
    num = k0*4892+42816
    num2 = (num<<7)^num
    for i in range(256):
        num = (num - k0 + num2) & 0xFFFFFFFF
        num2 = (num + 156) & 0xFFFFFFFF
        num = (num * (num2 & 206)) & 0xFFFFFFFF
        b[i] = num & 0xFF
        num >>= 3

def Data(item, fp, offest):
    start = offest["p"]
    with open(f'./dat/{item}.dat', 'rb') as f:
        f.seek(start)
        array = bytearray(f.read(offest["L"]))
        dd(array, offest["L"], offest["k"])
        os.makedirs(os.path.dirname(f'./data/{item}/{fp}'), exist_ok=True)
        with open(f'./data/{item}/{fp}', 'wb') as f:
            f.write(array)

for _ in os.listdir('./dat'):
    item = os.path.basename(_).split('.')[0]
    init(f'./dat/{item}.dat')
    with open(f'./json/{item}.json', 'w') as f:
        json.dump(ti, f, indent=4)
    with open(f'./json/{item}.json', 'r') as f:
        file = json.load(f)
        for key, value in file.items():
            Data(item, key, value)
    ti = {}