from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Importar configuración y registros de rutas
from config import Config
from models import db
from routes.location import location_bp
from routes.plant import plant_bp
from routes.image import image_bp
from routes.joins import join_bp
from routes.previous_research import previous_research_bp
from routes.use import use_bp
from routes.toponimo import toponimo_bp
from routes.interview_customer import interview_customer_bp
from routes.interview_vendor import interview_vendor_bp 

# Crear la aplicación Flask
app = Flask(__name__)
app.config.from_object(Config)

# Inicializar base de datos
db.init_app(app)

# Registrar Blueprints
app.register_blueprint(location_bp, url_prefix='/locations')
app.register_blueprint(plant_bp, url_prefix='/plants')
app.register_blueprint(image_bp, url_prefix='/images')
app.register_blueprint(previous_research_bp, url_prefix='/previous_researches')
app.register_blueprint(use_bp, url_prefix='/uses')
app.register_blueprint(toponimo_bp, url_prefix='/toponimos')
app.register_blueprint(interview_customer_bp, url_prefix='/interview_customers')
app.register_blueprint(interview_vendor_bp, url_prefix='/interview_vendors')
app.register_blueprint(join_bp)

# Crear tablas si no existen
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
