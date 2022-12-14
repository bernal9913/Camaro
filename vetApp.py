
from flask import Flask,flash, render_template,request,redirect,session
from funciones import *
from passlib.hash import sha256_crypt

app = Flask(__name__)
app.secret_key = "asdfvfñfes7u2nairfn"
diccionario_usuarios = lee_diccionario_csv('usuarios.csv')
lista_mascotas = crea_lista_mascotas('mascotas.csv')
lista_clientes = crea_lista_clientes('clientes.csv')

@app.route("/", methods=['GET','POST'])
def index():
        return render_template('Home.html')

#LOGIN entrar a la pagina con el usuario registrado
@app.route("/Sign-in", methods= ["GET","POST"])
def login():
    if request.method == 'GET':
        return render_template('Sign-in.html')

    elif request.method == 'POST':
            usuario = request.form['usuario']
            #print(diccionario_usuarios)
            if usuario in diccionario_usuarios:
                password_db = diccionario_usuarios[usuario]['contraseña'] # password guardado
                password_forma = request.form['password'] #password presentado
                #verificado = sha256_crypt.verify(password_forma,password_db)
                if (password_db == password_forma):
                    session['usuario'] = usuario
                    session['logged_in'] = True
                    # if 'ruta' in session:
                    #     ruta = session['ruta']
                    #     session['ruta'] = None
                    #     return redirect(ruta)
                    # else:
                    return redirect(f"/inicio/{usuario}")
                else:
                   # msg = f'El password de {usuario} no corresponde'
                   # return render_template('signin.html',mensaje=msg)
                    flash("contraseña incorrecta","warning")
                    return redirect('/Sign-in')
                   
            else:
               # msg = f'usuario {usuario} no existe'
                #return render_template('signin.html',mensaje=msg)
                flash("usuario incorrecto","warning")
                return redirect('/Sign-in')


#LOGOUT salir de la pagina
@app.route('/logout/', methods=['GET'])
def logout():
    if request.method == 'GET':
        session.clear()
        return redirect("/")
    
#Inicio o vista del usuario
@app.route('/inicio/')
@app.route('/inicio/<usuario>', methods = ['GET'])
def Inicio(usuario=''):
    if usuario in diccionario_usuarios and session:
        if request.method == 'GET':
            tipo = diccionario_usuarios[usuario]['tipo_usuario']
            usuario = diccionario_usuarios[usuario]['nombre_usuario']
            menu = crea_menu(tipo,usuario)
            print(menu)
            return render_template('inicio.html', menu=menu)

    else:
        return render_template('error-404.html')

#Crear nuevo usuario
@app.route('/add_user')
@app.route('/add_user/<usuario>', methods=['GET','POST'])
def add_user(usuario):
    if request.method == ['GET']:
        return render_template('add_user')
    if usuario in diccionario_usuarios and session:
        if request.method == 'GET':
            usuario = diccionario_usuarios[usuario]['nombre_usuario']
            return render_template('add_user.html')
        if request.method == 'POST':
            valor = request.form['agregar']
            if valor == 'Agregar':
                nombre_usuario = request.form['user']
                nombre = request.form['nombre']
                appat = request.form['appat']
                apmat = request.form['apmat']
                correo = request.form['mail']
                tipo_usuario = request.form['tipo_usuario']
                contraseña = request.form['password']
                if correo not in diccionario_usuarios:
                    agregar_usuario(nombre_usuario, nombre, appat, apmat, correo, tipo_usuario, contraseña)
                    tipo = diccionario_usuarios[usuario]['tipo_usuario']
                    usuario = diccionario_usuarios[usuario]['nombre_usuario']
                    menu = crea_menu(tipo,usuario)
                    return render_template('inicio.html', menu=menu )

#Crear nuevo cliente
@app.route('/AgregarCliente', methods=['GET','POST'])
def agregarCleinte():
    if session:
        usuario = session['usuario']
        if request.method == 'GET':
            return render_template('AgregarCliente.html')
        elif request.method == 'POST':
            nombre = request.form['nombre']
            appat = request.form['appat']
            apmat = request.form['apmat']
            correo = request.form['mail']
            agregar_cliente(nombre,appat,apmat, correo)
            return redirect(f"/clientes/{usuario}")

#clientes
@app.route('/clientes/')
@app.route('/clientes/<usuario>', methods = ['GET','POST'])
def clientes(usuario='lista'):
    if usuario in diccionario_usuarios and session:
        if request.method == 'GET':
            usuario = diccionario_usuarios[usuario]['tipo_usuario']
            lista_clientes = crea_lista_clientes('clientes.csv')
            return render_template('clientes.html', clientes = lista_clientes, usuario = usuario)
        elif request.method == 'POST':
            #se elimina mascota y se refresca pagina
            propietario = diccionario_usuarios[usuario]['usuario']
            nombre = request.form['nombre']
            eliminaMascota(propietario,nombre)
            lista_clientes = crea_lista_clientes('clientes.csv')
            return render_template('clientes.html',clientes = lista_clientes, usuario = session['usuario'])

    else:
        return render_template('error-404.html')

#Mascotas del cliente
@app.route('/mascotas/')
@app.route('/mascotas/<usuario>', methods = ['GET','POST'])
def mascotas(usuario='lista'):
    if usuario in diccionario_usuarios and session:
        if request.method == 'GET':
            usuario = diccionario_usuarios[usuario]['tipo_usuario']
            lista_mascotas = crea_lista_mascotas('mascotas.csv')
            return render_template('mascotas.html',mascotas = lista_mascotas, usuario = usuario)
        elif request.method == 'POST':
            #se elimina mascota y se refresca pagina
            propietario = diccionario_usuarios[usuario]['usuario']
            nombre = request.form['nombre']
            eliminaMascota(propietario,nombre)
            lista_mascotas = crea_lista_mascotas('mascotas.csv')
            return render_template('mascotas.html',mascotas = lista_mascotas, usuario = session['usuario'])

    else:
        return render_template('error-404.html')

@app.route('/AgregarMascota', methods = ['GET','POST'])
def AgregarMascota():
    if session:
        usuario = session['usuario']
        if request.method == 'GET':
            return render_template('AgregarMascota.html', usuario = usuario )
        elif request.method == 'POST':
            propietario = usuario
            nombre = request.form['nombre']
            raza = request.form['raza']
            sexo = request.form['sexo']
            Funcion_AgregaMascota(propietario,nombre,raza,sexo)
            return redirect(f"/mascotas/{usuario}")

@app.route('/citas')
@app.route('/citas/<usuario>', methods = ['GET','POST'])
def AgendarCita():
   return render_template('Agendarcita.html')

if __name__ == "__main__":
    app.run(debug=True)