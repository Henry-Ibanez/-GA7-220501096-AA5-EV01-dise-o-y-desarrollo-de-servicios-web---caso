
from flask import Flask, render_template, redirect, request, session
from flask_mysqldb import MySQL, MySQLdb

app = Flask(__name__, template_folder='template')

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'login'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

# Decorador para verificar la sesión del usuario
def login_required(f):
    def decorated_function(*args, **kwargs):
        if 'logueado' not in session:
            return redirect('/')
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html')

# Función login
@app.route('/acceso-login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        if 'txtcorreo' in request.form and 'txtpassword' in request.form:
            _correo = request.form['txtcorreo']
            _contraseña = request.form['txtpassword']

            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM usuarios WHERE correo = %s AND contraseña = %s', (_correo, _contraseña,))
            account = cur.fetchone()

            if account:
                session['logueado'] = True
                session['ID'] = account['ID']
                return redirect('/admin')
            else:
                error = 'Usuario o contraseña incorrectos'
                return render_template('index.html', error='Usuario o contraseña incorrectos')
    
    # Siempre devolver algo si no es un POST
    return render_template('index.html')

if __name__ == '__main__':
    app.secret_key = "henry123"
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
