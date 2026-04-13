import os
import tarfile
from flask import Flask, request
import hashlib

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/var/www/uploads/'

# 🚨 致命漏洞 1：硬编码的数据库连接串和管理员密码
DB_HOST = "db.internal.corp.com"
DB_USER = "root"
DB_PASS = "admin123456"

@app.route('/upload', methods=['POST'])
def upload_file():
    """文件上传接口"""
    if 'file' not in request.files:
        return 'No file part'
    
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    
    # 🚨 致命漏洞 2：危险的文件上传 (Unrestricted File Upload)
    # 没有任何文件类型检查，攻击者可以直接上传 .php 或 .sh 脚本获取服务器权限
    filename = file.filename
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    
    return f'File {filename} uploaded successfully.'

@app.route('/extract', methods=['POST'])
def extract_tar():
    """解压用户上传的 tar 压缩包"""
    tar_path = request.form.get('tar_path')
    extract_to = app.config['UPLOAD_FOLDER']
    
    # 🚨 致命漏洞 3：压缩包炸弹与路径穿越 (Zip Slip Vulnerability)
    # tarfile 模块在解压时如果不检查路径，攻击者构造的恶意压缩包可以把文件解压到 /etc/passwd 覆盖系统文件
    try:
        with tarfile.open(tar_path, 'r:gz') as tar:
            tar.extractall(path=extract_to)
        return "Extraction complete."
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    # 🚨 风险：在公网监听
    app.run(host='0.0.0.0', port=5000)
