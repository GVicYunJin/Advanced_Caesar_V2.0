from flask import Flask, render_template, request, jsonify
import hashlib

app = Flask(__name__)

ALLOWED_CHARS = ''.join(chr(i) for i in range(32, 127))  # 包括常见标点符号、数字、字母
for codepoint in range(0x4E00, 0x9FFF + 1):  # 汉字范围
    ALLOWED_CHARS += chr(codepoint)

def generate_shifts(key):
    return [(ord(char) + index) for index, char in enumerate(key)]

def expand_key_sha256(key, length):
    hash_object = hashlib.sha256(key.encode())
    return hash_object.hexdigest()[:length]

def expand_key_sha244(key, length):
    hash_object = hashlib.sha224(key.encode())
    return hash_object.hexdigest()[:length]

def encrypt_decrypt_once(text, key_shifts, allowed_chars, encrypt=True):
    charset_len = len(allowed_chars)
    result = []
    
    for i, char in enumerate(text):
        if char not in allowed_chars:
            result.append(char)
            continue

        shift = key_shifts[i % len(key_shifts)]
        shift = shift if encrypt else -shift
        idx = allowed_chars.index(char)
        new_idx = (idx + shift) % charset_len
        result.append(allowed_chars[new_idx])
    
    return ''.join(result)

def complex_encrypt(text, key):
    key_shifts = generate_shifts(key)
    first_encryption = encrypt_decrypt_once(text, key_shifts, ALLOWED_CHARS, encrypt=True)
    
    extended_key_sha256 = expand_key_sha256(key, len(first_encryption))
    extended_shifts_sha256 = generate_shifts(extended_key_sha256)
    second_encryption = encrypt_decrypt_once(first_encryption, extended_shifts_sha256, ALLOWED_CHARS, encrypt=True)
    
    extended_key_sha244 = expand_key_sha244(key, len(second_encryption))
    extended_shifts_sha244 = generate_shifts(extended_key_sha244)
    final_encryption = encrypt_decrypt_once(second_encryption, extended_shifts_sha244, ALLOWED_CHARS, encrypt=True)
    
    return final_encryption

def complex_decrypt(encrypted_text, key):
    extended_key_sha244 = expand_key_sha244(key, len(encrypted_text))
    extended_shifts_sha244 = generate_shifts(extended_key_sha244)
    second_decryption = encrypt_decrypt_once(encrypted_text, extended_shifts_sha244, ALLOWED_CHARS, encrypt=False)
    
    extended_key_sha256 = expand_key_sha256(key, len(second_decryption))
    extended_shifts_sha256 = generate_shifts(extended_key_sha256)
    first_decryption = encrypt_decrypt_once(second_decryption, extended_shifts_sha256, ALLOWED_CHARS, encrypt=False)
    
    key_shifts = generate_shifts(key)
    original_text = encrypt_decrypt_once(first_decryption, key_shifts, ALLOWED_CHARS, encrypt=False)
    
    return original_text

@app.route('/')
def index():
    return render_template('index.html')  # 渲染前端页面

@app.route('/encrypt', methods=['POST'])
def encrypt():
    data = request.get_json()
    text = data.get('text')
    key = data.get('key')
    encrypted_text = complex_encrypt(text, key)
    return jsonify({"encryptedText": encrypted_text})

@app.route('/decrypt', methods=['POST'])
def decrypt():
    data = request.get_json()
    text = data.get('text')
    key = data.get('key')
    decrypted_text = complex_decrypt(text, key)
    return jsonify({"decryptedText": decrypted_text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3333, debug=True)
