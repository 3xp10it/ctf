from z3 import *
import base64

def encrypt(plaintext, key):
    plaintext += '|'
    plaintext += key
    key = key*(len(plaintext)//len(key))
    key += key[:len(plaintext)-len(key)]

    cipher = ''.join(chr(ord(i)^ord(j)) for i,j in zip(plaintext, key))
    cipher = base64.b64encode(cipher.encode('ascii'))
    return cipher.decode('ascii')

#z=11,y=17
ceshi_encrypted=encrypt("lalalanihaoflag{8989082399}","11122233344455566")


timu_encrypted="BCU8EGwlJzAdBjAcGCgaFxgsNyEKIy9iOBxDLwFePVtEIj1kOxBsJisnCg1jHFd4HQ0GaSYnF2wuLDIKT2MJVjxVDA5pKScQOGEuOBkGYwFMeAYLSyg3chcjYSQ0Cg9jBld4AQsZPTEgCiImYiMKBDENTCtVAgQ7ZCUCPzUnNU8aJglKK1lEBSwyNxFsKiw+GEM3AF14FxEZJy08BGwyKjACBmMHXngURAYsJTxDLS8mcR8GNxxBeAUFGD1/chAjYS44GQZjHFA5AUhLLT07DSttYjkKQy4BXzABRBgoPWhDLS0ucQIaYwRRPhBISygoPkMhOGIiGxEmBl8sHUQcLDY3QysoNDQBQzcHGCwdAUsvLTwGPzViMg4WMA0YMRtECiUochckJGImABEvDBR4AQwOaSI7BCQ1YjcAEWMcUD1VKAIrISACOCgtP08MJUh1ORsPAicgfEMEJDA0TwowSEwwEEQbOy0oBmwnLSNPFysBS3gZAR0sKGhDKi0jNhQ3Kw1nNRQDAiobJQw+JR04HDw7B0olCS0vGyceIg4QLTIsC3swTTwe"

#encrypted=ceshi_encrypted
encrypted=timu_encrypted

cipher=base64.b64decode(encrypted.encode("ascii")).decode('ascii')
length=len(cipher)
cipher=[BitVecVal(ord(each),8) for each in cipher]
plain_line=[BitVec('p%d' % i,8) for i in range(length)]
key_line=[BitVec('k%d' % i,8) for i in range(length)]
prefix=[BitVecVal(ord(each),8) for each in "flag{"]
for y in range(1,length-7+1):
    for z in range(0,length-y-7+1):
        s=Solver()
        #s.add(plain_line[z:z+5]==prefix)
        s.add(plain_line[z]==prefix[0])
        s.add(plain_line[z+1]==prefix[1])
        s.add(plain_line[z+2]==prefix[2])
        s.add(plain_line[z+3]==prefix[3])
        s.add(plain_line[z+4]==prefix[4])
        for i in range(length):
            32<=plain_line[i]
            plain_line[i]<=126
            32<=key_line[i]
            key_line[i]<=126
        plain_line[-y-1]==ord('|')
        key=plain_line[-y:]
        for i in range(length):
            s.add(key_line[i]==key[i%y])
            s.add(plain_line[i]^key_line[i]==cipher[i])
        if s.check()==sat:
            answer=s.model()
            print(answer)
            key_line="".join([chr(answer[each].as_long()) for each in key_line])
            plain_line="".join([chr(answer[each].as_long()) for each in plain_line])
            print("key_line:")
            print(key_line)
            print("plain_line:")
            print(plain_line)
            input("Congratulations!")

        else:
            print("try key len:%d,'flag{' index:%d" % (y,z))
            continue

