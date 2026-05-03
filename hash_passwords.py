from app import create_app, mysql
from werkzeug.security import generate_password_hash

def hash_existing_passwords():
    app = create_app()
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, password FROM users")
        users = cur.fetchall()
        
        updated_count = 0
        for user in users:
            user_id = user[0]
            password = user[1]
            
            # Simple check to see if it's already a werkzeug hash (pbkdf2:sha256: or scrypt:)
            if not password.startswith('scrypt:') and not password.startswith('pbkdf2:sha256:'):
                hashed_pw = generate_password_hash(password)
                cur.execute("UPDATE users SET password = %s WHERE id = %s", (hashed_pw, user_id))
                updated_count += 1
                
        mysql.connection.commit()
        cur.close()
        print(f"Successfully hashed {updated_count} plaintext passwords in the database.")

if __name__ == '__main__':
    hash_existing_passwords()
