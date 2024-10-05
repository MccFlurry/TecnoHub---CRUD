from flask import Flask, render_template, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Ruta para el home
@app.route('/')
def home():
    if 'usuario' in session:
        return render_template('home.html')
    else:
        return redirect(url_for('login'))

# Ruta para el login
@app.route('/login')
def login():
    return render_template('login.html')

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
