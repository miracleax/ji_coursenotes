
import sys
from operator import methodcaller
import re
import numpy
from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto import Random


def strxor(a, b):
    """XOR two hex strings like "3eab" and "fef1"

    :Parameters:
      a : hex string
        the first parameter
      b : hex string
        the second parameter
    :Returns:
      hex format of a ^ b.
    """
    return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a[: len(b)], b[: len(a)])])


def BytesXor(b1, b2):
    return [a ^ b for a, b in zip(b1, b2)]


def ByteToHex(bins):
    return ''.join(["%02x" % x for x in bins]).strip()


def run():
    """
    main process
    """
    keys = [
        "140b41b22a29beb4061bda66b6747e14",
        "140b41b22a29beb4061bda66b6747e14",
        "36f18357be4dbd77f050515c73fcf9f2",
        "36f18357be4dbd77f050515c73fcf9f2"
    ]
    cipherTexts = [
        "4ca00ff4c898d61e1edbf1800618fb2828a226d160dad07883d04e008a7897ee2e4b7465d5290d0c0e6c6822236e1daafb94ffe0c5da05d9476be028ad7c1d81",
        "5b68629feb8606f9a6667670b75b38a5b4832d0f26e1ab7da33249de7d4afc48e713ac646ace36e872ad5fb8a512428a6e21364b0c374df45503473c5242a253",
        "69dda8455c7dd4254bf353b773304eec0ec7702330098ce7f7520d1cbbb20fc388d1b0adb5054dbd7370849dbf0b88d393f252e764f1f5f7ad97ef79d59ce29f5f51eeca32eabedd9afa9329",
        "770b80259ec33beb2561358a9f2dc617e46218c0a53cbeca695ae45faa8952aa0e311bde9d4e01726d3184c34451"
    ]
    blockSize = 16  # 16-byte encryption
    q1 = cbcDecrypt(keys[0], cipherTexts[0], blockSize)
    q2 = cbcDecrypt(keys[1], cipherTexts[1], blockSize)
    q3 = ctrDecrypt(keys[2], cipherTexts[2], blockSize)
    q4 = ctrDecrypt(keys[3], cipherTexts[3], blockSize)

    print("\n\nAnswers:")
    print("Q1. ", q1)
    print("Q2. ", q2)
    print("Q3. ", q3)
    print("Q4. ", q4)


# Do 2 variants of CTR decryption
def ctrDecrypt(key, cypherText, blockSize):
    """
    decrypt CTR cyphertext
    """
    res1 = ctrDecrypt1(key, cypherText, blockSize)
    res2 = ctrDecrypt2(key, cypherText, blockSize)
    print("1: ", res1)
    print("2: ", res2)
    return res1


def ctrDecrypt1(key, cypherText, blockSize):
    k = key.decode('hex')
    ct = cypherText.decode('hex')
    iv = ct[:blockSize]
    ct1 = ct[blockSize:]
    ctr = Counter.new(blockSize*8, initial_value=int(iv.encode('hex'), 16))
    obj = AES.new(k, AES.MODE_CTR, counter=ctr)
    paddedStr = obj.decrypt(ct1)
    # paddingAmount = ord(paddedStr[len(paddedStr)-1:])
    return paddedStr  # [:-paddingAmount]


def ctrDecrypt2(key, cypherText, blockSize):
    cypherTextBlocks = [cypherText[i:i+(blockSize*2)]
                        for i in range(0, len(cypherText), (blockSize*2))]
    iv = int(cypherTextBlocks.pop(0), 16)

    cypherTextBlocksDecoded = list(
        map(methodcaller("decode", "hex"), cypherTextBlocks))

    k = key.decode('hex')

    pt = ""

    i = 0
    for c in cypherTextBlocksDecoded:
        ctr = hex(iv+i << 64)[2:(2*blockSize)+2] 
        # print ctr
        encIV = AES.new(k, AES.MODE_ECB).encrypt(ctr)
        plaintext = BytesXor(encIV, c)
        # print plaintext
        i = i + 1
        pt = plaintext + pt

    # @todo something is wrong with this implementation
    return "?"  # pt

# Do 2 variants of CBC decryption


def cbcDecrypt(key, cypherText, blockSize):
    print("\nCBC decryption of key/cypher", key, " / ", cypherText)
    res1 = cbcDecrypt1(key, cypherText, blockSize)
    res2 = cbcDecrypt2(key, cypherText, blockSize)
    print("1: ", res1)
    print("2: ", res2)
    return res2

# CBC decryption variant 1 (use AES.MODE_CBC mode),


def cbcDecrypt1(key, cypherText, blockSize):
    k = key.decode('hex')
    ct = cypherText.decode('hex')
    iv = ct[:blockSize]
    ct1 = ct[blockSize:]
    obj = AES.new(k, AES.MODE_CBC, iv)
    paddedStr = obj.decrypt(ct1)
    paddingAmount = ord(paddedStr[len(paddedStr)-1:])
    return paddedStr[:-paddingAmount]


# CBC decryption variant 2 defines blocks self, encrypts per block (ECB mode) and xors with previous block => plaintext
def cbcDecrypt2(key, cypherText, blockSize):
    cypherTextBlocks = [cypherText[i:i+(blockSize*2)]
                        for i in range(0, len(cypherText), (blockSize*2))]
    cypherTextBlocksDecoded = list(
        map(methodcaller("decode", "hex"), cypherTextBlocks))
    # iv =  cypherTextBlocksDecoded.pop(0)
    k = key.decode('hex')

    pt = ""

    iter = len(cypherTextBlocksDecoded)
    for c in reversed(cypherTextBlocksDecoded):
        iter = iter - 1
        if(iter > 0):
            cipher = AES.new(k, AES.MODE_ECB).decrypt(c)
            plaintext = strxor(cipher, cypherTextBlocksDecoded[iter - 1])
            # print "[",iter,"]", c.encode('hex'), " => ", cipher.encode('hex'), plaintext
            pt = plaintext + pt

    paddingAmount = ord(pt[len(pt)-1:])

    return pt[:-paddingAmount]


# xor two strings of different lengths


if __name__ == "__main__":
    run()
