import time
from pryssa import pryssa
import pandas

def main():
    x = 3
    pryssa(x)
    time.sleep(10)
    a = x * 2
    # PRYSSA a
    print(a)

if __name__ == '__main__':
    main()
