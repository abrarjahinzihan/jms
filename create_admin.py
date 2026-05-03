from app import create_app, mysql
from werkzeug.security import generate_password_hash

def create_default_admin():
    app = create_app()
    with app.app_context():
        cur = mysql.connection.cursor()
        
        # Check if admin already exists
        cur.execute("SELECT * FROM users WHERE username = 'admin'")
        if cur.fetchone():
            print("Admin user already exists!")
            return

        username = 'admin'
        password = 'admin_password'
        role = 'admin'
        hashed_pw = generate_password_hash(password)
        
        cur.execute(
            "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
            (username, hashed_pw, role)
        )
        mysql.connection.commit()
        cur.close()
        print(f"Default admin created successfully!\nUsername: {username}\nPassword: {password}")

if __name__ == '__main__':
    create_default_admin()
