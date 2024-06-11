from flask import Flask, render_template, request, send_file
import base64

app = Flask(__name__)

def decode_base64(encoded_data):
    return base64.b64decode(encoded_data).decode('utf-8')

def caesar_cipher_decrypt(text, shift):
    decrypted_text = ''
    for char in text:
        if char.isalpha():
            ascii_offset = ord('A') if char.isupper() else ord('a')
            decrypted_char = chr((ord(char) - ascii_offset - shift) % 26 + ascii_offset)
            decrypted_text += decrypted_char
        else:
            decrypted_text += char
    return decrypted_text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'fileInput' not in request.files:
        return 'No file part'
    file = request.files['fileInput']
    if file.filename == '':
        return 'No selected file'
    encrypted_content = file.read().decode('utf-8')
    decrypted_content = caesar_cipher_decrypt(decode_base64(encrypted_content), 3)
    with open('uploads/' + file.filename, 'w') as f:
        f.write(decrypted_content)
    return 'File uploaded and decrypted successfully'

@app.route('/download/<filename>')
def download(filename):
    with open('uploads/' + filename, 'r') as f:
        encrypted_content = f.read()
    decrypted_content = caesar_cipher_decrypt(decode_base64(encrypted_content), 3)
    return send_file('uploads/' + filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
