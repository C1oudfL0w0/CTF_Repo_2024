import hashlib
from tqdm import tqdm

def md5_hash(text):
    return hashlib.md5(text.encode()).hexdigest()

target_hash = 'ca12fd8250972ec363a16593356abb1f3cf3a16d'
prefix = '188'

for i in tqdm(range(10000000, 100000000)):
    number = prefix + str(i).zfill(8)  # 以188开头，后面填充8位数字
    if md5_hash(number) == target_hash:
        print(f"Found: {number}")
        break