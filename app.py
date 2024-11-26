from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_mysqldb import MySQL

# Inicializar la app y Flask-Bcrypt
app = Flask(__name__)
bcrypt = Bcrypt(app)

# Configurar la base de datos MySQL
app.config['MYSQL_HOST'] = '127.0.0.1'  # Usa la dirección IP en lugar de 'localhost'
app.config['MYSQL_PORT'] = 3306        # Asegúrate de usar el puerto correcto
app.config['MYSQL_USER'] = 'db_login'
app.config['MYSQL_PASSWORD'] = 'easyfornow'
app.config['MYSQL_DB'] = 'users_db'

# Inicializar MySQL
mysql = MySQL(app)

#RUTA HELLO
@app.route('/', methods=['GET'])
def home():
    return jsonify(message="Hello, World!"), 200





# Ruta de login
@app.route('/login', methods=['POST'])
def login():
    print('paso')
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
    user = cursor.fetchone()
    cursor.close()

    if user:
        # Comparar contraseñas usando bcrypt
        if bcrypt.check_password_hash(user[1], password):  # `user[1]` es la contraseña encriptada
            return jsonify(message="Login exitoso"), 200
        else:
            return jsonify(message="Contraseña incorrecta"), 401
    else:
        return jsonify(message="Usuario no encontrado"), 401

# Ruta de registro de usuario
@app.route('/register', methods=['POST'])
def register():
    print('paso')
    data = request.get_json()
    
    username = data.get('username')
    password = data.get('password')
    print(password)
    # Verificar si el usuario ya existe
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
    user = cursor.fetchone()

    if user:
        cursor.close()
        return jsonify(message="El usuario ya existe"), 400

    # Encriptar la contraseña
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Insertar el nuevo usuario
    cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, hashed_password))
    mysql.connection.commit()
    cursor.close()

    return jsonify(message="Usuario registrado correctamente"), 201

if __name__ == '__main__':
    app.run(debug=True)
