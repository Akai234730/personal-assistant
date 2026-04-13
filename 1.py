import os
from flask import Flask, request, send_file

app = Flask(__name__)

# 🚨 致命漏洞 1：硬编码的机密信息 (JWT Secret / 云厂商 Token)
JWT_SECRET_KEY = "super_secret_jwt_key_123456_do_not_share"
AWS_S3_TOKEN = "AKIAIOSFODNN7EXAMPLE_TEST"

@app.route('/ping')
def ping_host():
    """测试服务器连通性的接口"""
    target_ip = request.args.get('ip')
    
    # 🚨 致命漏洞 2：操作系统命令注入 (OS Command Injection)
    # 没有任何过滤，攻击者可以输入 "127.0.0.1; rm -rf /" 来执行毁灭性命令
    result = os.popen(f"ping -c 3 {target_ip}").read()
    return result

@app.route('/download')
def download_file():
    """下载用户文件的接口"""
    filename = request.args.get('file')
    
    # 🚨 致命漏洞 3：目录穿越 / 任意文件读取 (Path Traversal)
    # 没有限制路径，攻击者可以输入 "../../../../etc/passwd" 来读取服务器的核心密码文件
    file_path = os.path.join("/var/www/uploads", filename)
    return send_file(file_path)

if __name__ == '__main__':
    # 🚨 致命风险：在生产环境开启了 debug 模式
    app.run(host='0.0.0.0', port=8080, debug=True)
