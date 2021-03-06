from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Habilitando el uso del ORM en la app flask mediante objeto "db"
db = SQLAlchemy(app)

  # postgresql://<nombre_usuario>:<contrasena>@host:puertos/<nombre_basededatos>'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://xdudnokqowutdf:f311089e8957a37f578905dbab008f637a69f6f1cd2b92596bf3957e13bbfef1@ec2-52-86-193-24.compute-1.amazonaws.com:5432/da40ajobl355co'
app.config['SQLAlCHEMY_TRACK_MODIFICATIONS'] = False

# adasda
class Notas(db.Model):
  '''Clase Notas'''
  __tablename__ = "notas"
  idNota = db.Column(db.Integer, primary_key = True)
  tituloNota = db.Column(db.String(80))
  cuerpoNota = db.Column(db.String(150))

  def __init__(self, tituloNota, cuerpoNota):
      self.tituloNota = tituloNota
      self.cuerpoNota = cuerpoNota
    

@app.route('/')
def index():
    objeto = { "nombre": "Mario",
              "apellido": "Cordova"
             }
    nombre = "Mario"
    
    lista_nombres = ["Alberto", "Mario", "Beto"] 
    
    return render_template( "index.html", variable = lista_nombres )

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/crearnota", methods=['POST'])
def crearnota():
    campotitulo = request.form["campotitulo"]
    campocuerpo = request.form["campocuerpo"]
    print(campotitulo)
    print(campocuerpo)
    notaNueva = Notas(tituloNota=campotitulo,cuerpoNota=campocuerpo)
    db.session.add(notaNueva)
    db.session.commit()

    return redirect("/leernotas")
    #return render_template("index.html", titulo = campotitulo, cuerpo = campocuerpo) 
   #return "Nota creada"

@app.route("/leernotas")
def leernotas():
    consulta_notas = Notas.query.all()
    print(consulta_notas)
    for nota in consulta_notas:
        titulo = nota.tituloNota
        cuerpo = nota.cuerpoNota
        print(nota.tituloNota)
        print(nota.cuerpoNota)  
    #return "Notas consultadas"
    return render_template("leerNotas.html", consulta = consulta_notas) 

@app.route("/eliminarnota/<id>")
def eliminar(id):
    nota = Notas.query.filter_by(idNota=int(id)).delete()
    print (nota)
    db.session.commit()
    return redirect("/leernotas")

@app.route("/edit/<id>")
def editar(id):
    nota = Notas.query.filter_by(idNota=int(id)).first()
    print(nota)
    print(nota.tituloNota)
    print(nota.cuerpoNota)
    return render_template("modificar.html", nota = nota )

@app.route("/modificarnota", methods= ['POST'])
def modificar():
    idnota = request.form['idnota']
    nuevo_titulo = request.form['campotitulo']
    nuevo_cuerpo = request.form['campocuerpo']
    nota = Notas.query.filter_by(idNota=int(idnota)).first()
    nota.tituloNota = nuevo_titulo 
    nota.cuerpoNota = nuevo_cuerpo
    db.session.commit()
    return redirect("/leernotas")


if __name__== "__main__":
    db.create_all()
    app.run()