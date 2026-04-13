import sqlite3

# 🚨 致命漏洞 1：硬编码的数据库密码和 API 密钥
DB_PASSWORD = "super_secret_admin_password_123!"
AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"

def get_user_data(user_id):
    """获取用户数据的 API 接口"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # 🚨 致命漏洞 2：裸奔的 SQL 拼接（极其容易被 SQL 注入）
    query = "SELECT * FROM users WHERE id = " + user_id
    
    cursor.execute(query)
    result = cursor.fetchall()
    
    conn.close()
    return result

if __name__ == "__main__":
    print("Test script initialized.")
