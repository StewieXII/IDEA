from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Crea la aplicación
app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave-super-secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/idea-bbdd'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar SQLAlchemy
db = SQLAlchemy(app)

# Inicializar LoginManager
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Importar las rutas y los modelos
from . import routes, models
