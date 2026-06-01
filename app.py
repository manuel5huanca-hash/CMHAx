from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user

# Crear la aplicación Flask
app = Flask(__name__)
app.secret_key = "clave_secreta"

# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Usuario fijo
usuarios = {"Cesar": {"password": "Huanquita15."}}

# Contador de intentos
intentos = 0
MAX_INTENTOS = 3

class Usuario(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return Usuario(user_id)

# Lista de productos (ejemplo)
productos = [
    {"nombre": "Laptop Gamer", "precio": "S/ 3,200", "imagen": "laptop.png"},
    {"nombre": "Monitor 27''", "precio": "S/ 950", "imagen": "monitor.webp"},
    {"nombre": "Procesador", "precio": "S/ 1,200", "imagen": "procesador.png"},
    {"nombre": "Tarjeta Gráfica", "precio": "S/ 1,800", "imagen": "grafica.png"},
]

# Página principal
@app.route('/')
def inicio():
    return render_template('index.html', productos=productos)

# Login con 3 intentos
@app.route('/login', methods=['GET', 'POST'])
def login():
    global intentos
    if request.method == 'POST':
        nombre = request.form['username']
        clave = request.form['password']

        # Bloqueo si excede intentos
        if intentos >= MAX_INTENTOS:
            return render_template('bloqueo.html')

        # Validación usuario/clave
        if nombre in usuarios and usuarios[nombre]['password'] == clave:
            user = Usuario(nombre)
            login_user(user)
            intentos = 0  # Reinicia intentos al iniciar sesión correctamente
            flash("✅ Inicio de sesión exitoso", "success")
            return redirect(url_for('inicio'))
        else:
            intentos += 1
            restantes = MAX_INTENTOS - intentos
            flash(f"❌ Usuario o contraseña incorrectos — Intentos restantes: {restantes}", "danger")

    return render_template('login.html')

# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("👋 Sesión cerrada", "info")
    return redirect(url_for('inicio'))

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
