import rsa
import time
from tkinter import *
import tkinter.messagebox
import tkinter as tk
from pyDes import des, CBC, PAD_PKCS5
import binascii
import numpy as np
from PIL import Image
from PIL import ImageTk

# DES密钥
with open(r"C:\Users\zjq13\Desktop\资料\密码学大作业\key.txt",'r') as f:
    KEY = f.read()
key = rsa.newkeys(1024)  # 生成随机密钥
privateKeyB = key[1]  # B的私钥
publicKeyB = key[0]  # B的公钥

def des_encrypt(s):
    """
    DES 加密
    :param s: 原始字符串
    :return: 加密后字符串，16进制
    """
    secret_key = KEY
    iv = secret_key
    k = des(secret_key, CBC, iv, pad=None, padmode=PAD_PKCS5)
    en = k.encrypt(s, padmode=PAD_PKCS5)
    return binascii.b2a_hex(en)


def des_descrypt(s):
    """
    DES 解密
    :param s: 加密后的字符串，16进制
    :return:  解密后的字符串
    """
    secret_key = KEY
    iv = secret_key
    k = des(secret_key, CBC, iv, pad=None, padmode=PAD_PKCS5)
    de = k.decrypt(binascii.a2b_hex(s), padmode=PAD_PKCS5)
    return de

def main1():
    # RSA加解密
    # 公钥加密
    # 加密时间测量
    start_time = time.time()
    message = KEY
    print('加密的DES的秘钥：', message)
    message = message.encode()
    global cryptedMessage
    cryptedMessage = rsa.encrypt(message, publicKeyB)
    print("加密后的对称密钥的bytes形式：",cryptedMessage)
    with open(r"C:\Users\zjq13\Desktop\资料\密码学大作业\miku.txt", "w") as f:
        f.write(cryptedMessage.hex())
    print('加密后的对称密钥的十六进制形式：', cryptedMessage.hex())
    txt1.insert(END, 'DES加密后结果: ')
    txt1.insert(END, '\n')
    txt1.insert(END, cryptedMessage.hex())
    txt1.insert(END, '\n' + '\n' + '\n')
    txt1.update()
    end_time = time.time()
    print(f"DES密钥加密过程花费时间: {end_time - start_time} 秒")

    #发送的明文
    start_time = time.time()
    with open(r"C:\Users\zjq13\Desktop\资料\密码学大作业\bbb.txt",'r') as f:
        s=f.read()
    print("\n")
    enc = des_encrypt(s)
    print ("DES加密后的密文：")
    print(enc)
    enc1 = str(enc, encoding="utf8")
    with open(r"C:\Users\zjq13\Desktop\资料\密码学大作业\aaa.txt",'w') as f:
        f.write(enc1)
    txt1.insert(END, 'Alice发送的密文: ')
    txt1.insert(END, '\n')
    txt1.insert(END, enc1)
    txt1.insert(END, '\n'+'\n'+'\n')
    txt1.update()
    tk.messagebox.askokcancel(title='提示', message='Alice传输密文成功\n请等待图片加密完成，约20秒左右')

    #图片转二进制
    im = Image.open(r"C:\Users\zjq13\Desktop\资料\密码学大作业\picture5.jpg")
    im2 = np.array(im)
    np.save(file=r"C:\Users\zjq13\Desktop\资料\密码学大作业\out.npy", arr=im2)
    #加密二进制
    with open(r"C:\Users\zjq13\Desktop\资料\密码学大作业\out.npy",'rb') as f:
        ai=f.read()
    encc = des_encrypt(ai)
    with open(r"C:\Users\zjq13\Desktop\资料\密码学大作业\oout.npy",'wb') as f:
        f.write(encc)
    print("DES加密后的图片二进制：")
    print(encc)
    print('\n')
    tk.messagebox.askokcancel(title='提示', message='Alice传输图片密文成功')
    tk.messagebox.askokcancel(title='提示', message='Alice传输图片密文成功')
    end_time = time.time()
    print(f"文本和图片加密过程花费时间: {end_time - start_time} 秒")

def main2():
    # RSA加解密
    start_time = time.time()
    with open(r"C:\Users\zjq13\Desktop\资料\密码学大作业\miku.txt","r") as f:
        meassage1=f.read()
    print("文件中对称密钥的十六进制:",meassage1)
    meassage2=bytes(meassage1,encoding="utf-8")
    print("文件中对称密钥的bytes形式：",meassage2)
    # 私钥解密
    message = rsa.decrypt(cryptedMessage, privateKeyB)
    message = message.decode()
    print('解密后：', message)

    txt2.insert(END, '解密得到DES的秘钥：')
    txt2.insert(END, '\n')
    txt2.insert(END, message)
    txt2.insert(END, '\n'+'\n'+'\n')
    txt2.update()
    end_time = time.time()
    print(f"DES密钥解密过程花费时间: {end_time - start_time} 秒")

    #发送的密文
    start_time = time.time()
    with open(r"C:\Users\zjq13\Desktop\资料\密码学大作业\aaa.txt",'r') as f:
        s=f.read()
    print(s)
    print("\n")
    enc = s
    print ("DES加密后的密文：")
    print(enc)
    des = des_descrypt(enc)
    print ("DES解密后的明文：")
    print(des)
    des1 = str(des, encoding="utf8")
    txt2.insert(END, 'Bob解密的明文: ')
    txt2.insert(END, '\n')
    txt2.insert(END, des1)
    txt2.insert(END, '\n'+'\n'+'\n')
    txt2.update()
    print("\n")
    tk.messagebox.askokcancel(title='提示', message='Bob接收成功\n请等待，正在解密图片')

    #解密图片二进制数组
    with open(r"C:\Users\zjq13\Desktop\资料\密码学大作业\oout.npy",'rb') as f:
        ss=f.read()
    dess = des_descrypt(ss)
    with open(r"C:\Users\zjq13\Desktop\资料\密码学大作业\oout.npy",'wb') as f:
        f.write(dess)
    #转为图片
    ai2=np.load(r"C:\Users\zjq13\Desktop\资料\密码学大作业\oout.npy")
    print(ai2)
    image = Image.fromarray(ai2)
    image.save('yt.png')
    end_time = time.time()
    print(f"文本和图片解密过程花费时间: {end_time - start_time} 秒")
    tk.messagebox.askokcancel(title='提示', message='图片转换成功，即将显示')
    img = Image.open("yt.png")
    img.show()

#TKinter
root = tk.Tk()
root.geometry('600x400')
root.title('密码学实验交互界面')
canvas = tk.Canvas(root, width=1900, height=750, bd=0, highlightthickness=0)
imgpath = r"C:\Users\zjq13\Desktop\资料\密码学大作业\picture.jpg"
img = Image.open(imgpath)
photo = ImageTk.PhotoImage(img)

canvas.create_image(500, 300, image=photo)
canvas.pack()


btn1 = Button(root, text='Alice开始加密传输',bg='grey',command=main1,fg='white')
txt1 = Text(root)
txt1.place(relx=0.4, rely=0.1, relwidth=0.5, relheight=0.35)
btn1.place(relx=0.05, rely=0.1, relwidth=0.3, relheight=0.2)

btn2 = Button(root, text='Bob开始解密', bg='grey',command=main2,fg='white')
txt2 = Text(root)
txt2.place(relx=0.4, rely=0.5, relwidth=0.5, relheight=0.35)
btn2.place(relx=0.05, rely=0.5, relwidth=0.3, relheight=0.2)

root.mainloop()