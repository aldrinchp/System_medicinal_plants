from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()
class Image(db.Model):
    __tablename__ = 'images'     
    id = db.Column(db.Integer, primary_key=True)
    plant_id = db.Column(db.Integer, db.ForeignKey('plants.id'), nullable=False)

    date = db.Column(db.Date, nullable=False, default=date.today)
    place = db.Column(db.String(100)) 

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, plant_id, date,place):
        self.plant_id = plant_id
        self.date = date
        self.place = place

    def __repr__(self):
        return 'Image %d>' % self.id


class Plant(db.Model):
    __tablename__ = 'plants'     
    id = db.Column(db.Integer, primary_key=True)

    # Clave foránea que referencia a la tabla 'Site_Origin'
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)

    current_name = db.Column(db.String(100))
    scientific_name = db.Column(db.String(100))

    images = db.relationship('Image', backref='plants', lazy=True, cascade='all, delete-orphan')
    previous_researches = db.relationship('PreviousResearch', backref='plants', lazy=True, cascade='all, delete-orphan')
    uses = db.relationship('Use', backref='plants', lazy=True, cascade='all, delete-orphan')
    toponimos = db.relationship('Toponimo', backref='plants', lazy=True, cascade='all, delete-orphan')

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, location_id,current_name,scientific_name):
        self.location_id = location_id
        self.current_name = current_name
        self.scientific_name = scientific_name

    def __repr__(self):
        return 'Plant %d>' % self.id



class Location(db.Model):
    __tablename__ = 'locations'     
    id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(100))
    id_province = db.Column(db.Integer)

    plants = db.relationship('Plant', backref='locations', lazy=True, cascade='all, delete-orphan')
    interview_customers = db.relationship('InterviewCustomer', backref='locations', lazy=True, cascade='all, delete-orphan')
    interview_vendors = db.relationship('InterviewVendor', backref='locations', lazy=True, cascade='all, delete-orphan')

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, city_name,id_province):
        self.city_name = city_name
        self.id_province = id_province

    def __repr__(self):
        return 'Location %d>' % self.id


class PreviousResearch(db.Model):
    __tablename__ = 'previous_researches'
    id = db.Column(db.Integer, primary_key=True)
    id_plant = db.Column(db.Integer, db.ForeignKey('plants.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    link = db.Column(db.String(255), nullable=False)

    def __init__(self, id_plant, title, link):
        self.id_plant = id_plant
        self.title = title
        self.link = link

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __repr__(self):
        return '<PreviousResearch %d: %s>' % (self.id_research, self.title)


class Use(db.Model):
    __tablename__ = 'uses'
    id = db.Column(db.Integer, primary_key=True)
    id_plant = db.Column(db.Integer, db.ForeignKey('plants.id'), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    type_use = db.Column(db.String(100), nullable=False)

    def __init__(self, id_plant, description, type_use):
        self.id_plant = id_plant
        self.description = description
        self.type_use = type_use

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __repr__(self):
        return '<Use %d: %s>' % (self.id_use, self.description)


class Toponimo(db.Model):
    __tablename__ = 'toponimos'
    
    id = db.Column(db.Integer, primary_key=True)
    id_plant = db.Column(db.Integer, db.ForeignKey('plants.id'), nullable=False)
    origin = db.Column(db.String(255), nullable=False)
    comercial_distribution = db.Column(db.String(255), nullable=False)
    distribution = db.Column(db.String(255), nullable=False)


    def __init__(self, id_plant, origin, comercial_distribution, distribution):
        self.id_plant = id_plant
        self.origin = origin
        self.comercial_distribution = comercial_distribution
        self.distribution = distribution

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __repr__(self):
        return '<Toponimo %d: %s>' % (self.id_toponimo, self.origin)

class InterviewCustomer(db.Model):
    __tablename__ = 'interview_customers'
    
    id = db.Column(db.Integer, primary_key=True)
    id_location = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    link = db.Column(db.String(500), nullable=False)
    
    # Campos q1 a q24 como varchar
    q1 = db.Column(db.String(255), nullable=False)
    q2 = db.Column(db.String(255), nullable=False)
    q3 = db.Column(db.String(255), nullable=False)
    q4 = db.Column(db.String(255), nullable=False)
    q5 = db.Column(db.String(255), nullable=False)
    q6 = db.Column(db.String(255), nullable=False)
    q7 = db.Column(db.String(255), nullable=False)
    q8 = db.Column(db.String(255), nullable=False)
    q9 = db.Column(db.String(255), nullable=False)
    q10 = db.Column(db.String(255), nullable=False)
    q11 = db.Column(db.String(255), nullable=False)
    q12 = db.Column(db.String(255), nullable=False)
    q13 = db.Column(db.String(255), nullable=False)
    q14 = db.Column(db.String(255), nullable=False)
    q15 = db.Column(db.String(255), nullable=False)
    q16 = db.Column(db.String(255), nullable=False)
    q17 = db.Column(db.String(255), nullable=False)
    q18 = db.Column(db.String(255), nullable=False)
    q19 = db.Column(db.String(255), nullable=False)
    q20 = db.Column(db.String(255), nullable=False)
    q21 = db.Column(db.String(255), nullable=False)
    q22 = db.Column(db.String(255), nullable=False)
    q23 = db.Column(db.String(255), nullable=False)
    q24 = db.Column(db.String(255), nullable=False)

    def __init__(self, id_location,link, **kwargs):
        self.id_location = id_location
        self.link = link
        for i in range(1, 25):  # Asignar los valores de q1 a q23 dinámicamente
            setattr(self, f'q{i}', kwargs.get(f'q{i}', None))

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __repr__(self):
        return '<InterviewCustomer %d: Location ID %d>' % (self.id, self.id_location)


class InterviewVendor(db.Model):
    __tablename__ = 'interview_vendors'
    
    id = db.Column(db.Integer, primary_key=True)
    id_location = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    link = db.Column(db.String(500), nullable=False)
    
    # Campos q1 a q23 como varchar
    q1 = db.Column(db.String(255), nullable=False)
    q2 = db.Column(db.String(255), nullable=False)
    q3 = db.Column(db.String(255), nullable=False)
    q4 = db.Column(db.String(255), nullable=False)
    q5 = db.Column(db.String(255), nullable=False)
    q6 = db.Column(db.String(255), nullable=False)
    q7 = db.Column(db.String(255), nullable=False)
    q8 = db.Column(db.String(255), nullable=False)
    q9 = db.Column(db.String(255), nullable=False)
    q10 = db.Column(db.String(255), nullable=False)
    q11 = db.Column(db.String(255), nullable=False)
    q12 = db.Column(db.String(255), nullable=False)
    q13 = db.Column(db.String(255), nullable=False)
    q14 = db.Column(db.String(255), nullable=False)
    q15 = db.Column(db.String(255), nullable=False)
    q16 = db.Column(db.String(255), nullable=False)
    q17 = db.Column(db.String(255), nullable=False)
    q18 = db.Column(db.String(255), nullable=False)
    q19 = db.Column(db.String(255), nullable=False)
    q20 = db.Column(db.String(255), nullable=False)
    q21 = db.Column(db.String(255), nullable=False)
    q22 = db.Column(db.String(255), nullable=False)
    q23 = db.Column(db.String(255), nullable=False)
    

    def __init__(self, id_location,link, **kwargs):
        self.id_location = id_location
        self.link = link
        for i in range(1, 24):  # Asignar los valores de q1 a q23 dinámicamente
            setattr(self, f'q{i}', kwargs.get(f'q{i}', None))
        

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __repr__(self):
        return '<InterviewVendor %d: Location ID %d>' % (self.id, self.id_location)
