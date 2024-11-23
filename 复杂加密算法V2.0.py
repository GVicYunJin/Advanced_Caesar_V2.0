import hashlib
import tkinter as tk
from tkinter import messagebox, scrolledtext

# 动态生成包含所有汉字及常见符号的字符集
def generate_allowed_chars():
    # 包括所有常见可打印字符（ASCII 32-126）和汉字（\u4E00-\u9FFF）
    allowed_chars = ''.join(chr(i) for i in range(32, 127))  # 包括常见标点符号、数字、字母
    for codepoint in range(0x4E00, 0x9FFF + 1):  # 汉字范围
        allowed_chars += chr(codepoint)
    return allowed_chars

ALLOWED_CHARS = generate_allowed_chars()

def generate_shifts(key):
    """生成基于密钥的偏移序列。"""
    return [(ord(char) + index) for index, char in enumerate(key)]

def expand_key_sha256(key, length):
    """使用 SHA-256 扩展密钥，截取指定长度。"""
    hash_object = hashlib.sha256(key.encode())
    return hash_object.hexdigest()[:length]

def expand_key_sha244(key, length):
    """使用 SHA-224 扩展密钥，截取指定长度。"""
    hash_object = hashlib.sha224(key.encode())
    return hash_object.hexdigest()[:length]

def encrypt_decrypt_once(text, key_shifts, allowed_chars, encrypt=True):
    """单轮加密或解密操作。"""
    charset_len = len(allowed_chars)
    result = []
    
    for i, char in enumerate(text):
        if char not in allowed_chars:
            result.append(char)  # 非字符集字符直接保留
            continue

        shift = key_shifts[i % len(key_shifts)]
        shift = shift if encrypt else -shift
        idx = allowed_chars.index(char)
        new_idx = (idx + shift) % charset_len
        result.append(allowed_chars[new_idx])
    
    return ''.join(result)

def complex_encrypt(text, key):
    """执行三轮加密。"""
    # 第一次加密
    key_shifts = generate_shifts(key)
    first_encryption = encrypt_decrypt_once(text, key_shifts, ALLOWED_CHARS, encrypt=True)
    
    # 第二次加密（SHA-256扩展密钥）
    extended_key_sha256 = expand_key_sha256(key, len(first_encryption))
    extended_shifts_sha256 = generate_shifts(extended_key_sha256)
    second_encryption = encrypt_decrypt_once(first_encryption, extended_shifts_sha256, ALLOWED_CHARS, encrypt=True)
    
    # 第三次加密（SHA-224扩展密钥）
    extended_key_sha244 = expand_key_sha244(key, len(second_encryption))
    extended_shifts_sha244 = generate_shifts(extended_key_sha244)
    final_encryption = encrypt_decrypt_once(second_encryption, extended_shifts_sha244, ALLOWED_CHARS, encrypt=True)
    
    return final_encryption

def complex_decrypt(encrypted_text, key):
    """执行三轮解密，顺序与加密相反。"""
    # 第三次解密（SHA-224扩展密钥）
    extended_key_sha244 = expand_key_sha244(key, len(encrypted_text))
    extended_shifts_sha244 = generate_shifts(extended_key_sha244)
    second_decryption = encrypt_decrypt_once(encrypted_text, extended_shifts_sha244, ALLOWED_CHARS, encrypt=False)
    
    # 第二次解密（SHA-256扩展密钥）
    extended_key_sha256 = expand_key_sha256(key, len(second_decryption))
    extended_shifts_sha256 = generate_shifts(extended_key_sha256)
    first_decryption = encrypt_decrypt_once(second_decryption, extended_shifts_sha256, ALLOWED_CHARS, encrypt=False)
    
    # 第一次解密
    key_shifts = generate_shifts(key)
    original_text = encrypt_decrypt_once(first_decryption, key_shifts, ALLOWED_CHARS, encrypt=False)
    
    return original_text

# GUI 部分
def encrypt_action():
    """加密操作。"""
    text = input_text.get("1.0", tk.END).strip()
    key = key_entry.get()
    if not text or not key:
        messagebox.showerror("错误", "请输入文本和密钥！")
        return
    encrypted_text = complex_encrypt(text, key)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, encrypted_text)

def decrypt_action():
    """解密操作。"""
    text = input_text.get("1.0", tk.END).strip()
    key = key_entry.get()
    if not text or not key:
        messagebox.showerror("错误", "请输入文本和密钥！")
        return
    decrypted_text = complex_decrypt(text, key)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, decrypted_text)

# 创建主窗口
root = tk.Tk()
root.title("复杂加密算法工具V2.0")

# 输入文本
tk.Label(root, text="输入文本：").grid(row=0, column=0, padx=5, pady=5, sticky="w")
input_text = scrolledtext.ScrolledText(root, width=50, height=10)
input_text.grid(row=0, column=1, padx=5, pady=5)

# 输入密钥
tk.Label(root, text="密钥：").grid(row=1, column=0, padx=5, pady=5, sticky="w")
key_entry = tk.Entry(root, width=30)
key_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

# 输出文本
tk.Label(root, text="输出结果：").grid(row=2, column=0, padx=5, pady=5, sticky="w")
output_text = scrolledtext.ScrolledText(root, width=50, height=10)
output_text.grid(row=2, column=1, padx=5, pady=5)

# 按钮
encrypt_button = tk.Button(root, text="加密", command=encrypt_action, width=10)
encrypt_button.grid(row=3, column=0, padx=5, pady=10)

decrypt_button = tk.Button(root, text="解密", command=decrypt_action, width=10)
decrypt_button.grid(row=3, column=1, padx=5, pady=10, sticky="w")

# 运行主循环
root.mainloop()
