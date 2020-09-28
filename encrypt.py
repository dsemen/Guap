# coding: utf-8
import tkinter.filedialog
import tkinter as tk
import random
from uuid import uuid4
import numpy as np

# Interface functions
def insertText():
    """read text from file and insert it to textbox 'Исходный текст'"""
    txt1.delete(1.0, tk.END)
    file_name = tk.filedialog.askopenfilename()
    f = open(file_name)
    s = f.read()
    txt1.insert(1.0, s)
    f.close()
    
def saveText():
    """Save text from textbox 'Результат' to file"""
    file_name = tk.filedialog.asksaveasfilename(filetypes=(("TXT files", "*.txt"),
                                        ("HTML files", "*.html;*.htm"),
                                                ("All files", "*.*") ))
    f = open(file_name, 'w')
    s = txt2.get(1.0, tk.END)
    f.write(s)
    f.close()
    txt2.delete(1.0, tk.END)

def ins_encrypted():
    #get text to encrypt
    mystr = txt1.get(1.0, tk.END)
    #set encryption key and encrypt
    set_value(mystr)
    #copy to textbox2
    encr_txt = encrypt(mystr)
    txt2.insert(1.0, encr_txt)

def ins_decrypted():
    #get text to decrypt
    mystr = txt1.get(1.0, tk.END)
    #prepare data and decrypt
    lst = [int(x) for x in mystr[:-1].split()]
    #copy to textbox2
    s = decrypt(lst)
    txt2.insert(1.0, s)

# Process functions    
class Key:
    """Encryption key"""
    value = 0
    
    def __init__(self, value):
        Key.value = value
        
def set_value(string):        
    """Return list which will be used as key"""
    unique = list(set(string))
    min_num = sorted([string.count(x) for x in unique])[-1]
    key = (unique * min_num + list(uuid4().hex))  * random.randint(3, 10)
    random.shuffle(key)
    Key.value = key

def encrypt(string):
    """Encrypt string using key-string"""
    key_dict = dict(zip(list(set(string)), [np.where(np.array(list(Key.value)) == x)[0] for x in list(set(string))]))
    return [key_dict[y][y.count(string[:(x + 1)])] for (x, y) in list(enumerate(string))]
    
def decrypt (lst):
    """Decrypt string using key-string"""
    empty = ' '
    result = empty.join(str(Key.value[x]) for x in lst)
    return(result)    

# Create objects
window = tk.Tk()
window.title('Шифратор и дешифратор на основе алгоритма "БЛОКНОТ"')
window.geometry('810x610')
window.resizable(width=False, height=False)
f = Frame(window, width=800, height=400)

labe1 = tk.Label(f, text="Исходный текст:" )
labe2 = tk.Label(f, text="Результат:" )

txt1 = tk.Text(f, width=40, height=30, borderwidth=2)
txt2 = tk.Text(f, width=40, height=30, borderwidth=2)

encryptb = tk.Button(f, text="Зашифровать", command=ins_encrypted)
decryptb = tk.Button(f, text="Расшифровать", command=ins_decrypted)
insertTextb = tk.Button(f, text="Загрузить текст", command=insertText)
saveTextb = tk.Button(f, text="Сохранить текст", command=saveText)

# Place objects
labe1.grid(column=2, row=0)
labe2.grid(column=6, row=0)
txt1.grid(column=1, row=1, columnspan=3)
txt2.grid(column=5, row=1, columnspan=3)
encryptb.grid(column=2, row=3)
decryptb.grid(column=4, row=3)
insertTextb.grid(column=6, row=3)
saveTextb.grid(column=6, row=4)
f.pack()
window.mainloop()
