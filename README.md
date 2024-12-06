# Sistema de base de datos para plantas medicinales de la provincia de Imbabura

Este proyecto es una API diseñada para crear, gestionar y administrar las tablas de una base de datos relacional SQL sobre un conjunto de plantas medicinales de la provincia de Imbabura y  asi mismo los registros adherentes a ellas.

---

## Características

- **Insertar nuevos registros**: Los usuarios pueden insertar nuevos registros de las plantas y asi mismo informacion relacionada a ellas como entrevistas.
- **Creacion de tablas**:   La API tiene la capacidad de crear instantaneamente las tablas de la estrucctura relacional.
- **Obtencion de datos**: Los usuarios pueden obtener datos de la estrucctura relacional a travez de los comandos curls o usando Postman.
- **Modificacion de datos**: Los usuarios pueden modificar y actualizar los datos de un registro en especifico.
- **Joins entre tablas**: Los usuarios pueden realizar consultas del tipo join entre dos tablas, ademas de un join entre 3 tablas.

---

## Estructura de la Base de Datos

El sistema utiliza una base de datos relacional con las siguientes tablas principales:

- **Plants**: Detalla el nombre comun, nombre cientifico y lugar donde se realizó la busqueda de la informacion.
- **Locations**: Registra el nombre del canton y un id de provincia que puede ser variable o constante.
- **Images**: Contiene los registros de las imagenes asociadas a las plantas, ademas de su fecha y lugar donde se tomó la foto. 
- **Uses**: Describe el uso que se le da a una planta, asi como el tipo de uso que es.
- **Previous_researches**: Refiere a las investigaciones previas realizadas a una planta especifica, ademas incluye la informacion sobre el nombre y el link asociado
- **Toponimos**: Relaciona una planta a travez del lugar de origen, distribucion y distribucion comercial. 
- **Interview_customers**: Refiere a las entrevistas a consumidores relacionadas a donde se realizó la investigacion, contiene un link a la entrevista digital y las pregunas asociadas.
- **Interview_vendors**: Refiere a las entrevistas a vendedores relacionadas a donde se realizó la investigacion, contiene un link a la entrevista digital y las pregunas asociadas.
---

## Esquema de la base de datos

### Tabla: Plants

| **Field**       | **Type**     |**Null** | **Key** | **Default** | **Extra**      |
|-----------------|--------------|---------|---------|-------------|----------------|
| id              | int          | NO      | PRI     | NULL        | auto_increment |
| location_id     | int          | NO      | MUL     | NULL        |                |
| current_name    | varchar(100) | YES     |         | NULL        |                |
| scientific_name | varchar(100) | YES     |         | NULL        |                |

---

### Tabla: locations


| **Field**   | **Type**     | **Null** | **Key** | **Default** | **Extra**      |
|-------------|--------------|----------|---------|-------------|----------------|
| id          | int          | NO       | PRI     | NULL        | auto_increment |
| city_name   | varchar(100) | YES      |         | NULL        |                |
| id_province | int          | YES      |         | NULL        |                |

---

### Tabla: Images

| **Field**| **Type**     | **Null** | **Key** | **Default** | **Extra**       |
|----------|--------------|----------|---------|-------------|-----------------|
| id       | int          | NO       | PRI     | NULL        | auto_increment  |
| plant_id | int          | NO       | MUL     | NULL        |                 |
| date     | date         | NO       |         | NULL        |                 |
| place    | varchar(100) | YES      |         | NULL        |                 |

---

### Tabla: Uses

| **Field**   | **Type**     | **Null** | **Key** | **Default** | **Extra**      |
|-------------|--------------|----------|---------|-------------|----------------|
| id          | int          | NO       | PRI     | NULL        | auto_increment |
| id_plant    | int          | NO       | MUL     | NULL        |                |
| description | varchar(255) | NO       |         | NULL        |                |
| type_use    | varchar(100) | NO       |         | NULL        |                |


---

### Tabla: Previous_researches

| **Field**| **Type**     |**Null** | **Key** | **Default** | **Extra**      |
|----------|--------------|---------|---------|-------------|----------------|
| id       | int          | NO      | PRI     | NULL        | auto_increment |
| id_plant | int          | NO      | MUL     | NULL        |                |
| title    | varchar(255) | NO      |         | NULL        |                |
| link     | varchar(255) | NO      |         | NULL        |                |



### Tabla: Toponimos

| **Field**              | **Type**     | **Null** | **Key** | **Default** | **Extra**      |
|------------------------|--------------|----------|---------|-------------|----------------|
| id                     | int          | NO       | PRI     | NULL        | auto_increment |
| id_plant               | int          | NO       | MUL     | NULL        |                |
| origin                 | varchar(255) | NO       |         | NULL        |                |
| comercial_distribution | varchar(255) | NO       |         | NULL        |                |
| distribution           | varchar(255) | NO       |         | NULL        |                |

---

### Tabla: Interview_customers

| **Field**   |  **Type**    | **Null** | **Key** | **Default** | **Extra**      |
|-------------|--------------|----------|---------|-------------|----------------|
| id          | int          | NO       | PRI     | NULL        | auto_increment |
| id_location | int          | NO       | MUL     | NULL        |                |
| link        | varchar(500) | NO       |         | NULL        |                |
| q1          | varchar(255) | NO       |         | NULL        |                |
| q2          | varchar(255) | NO       |         | NULL        |                |
| q3          | varchar(255) | NO       |         | NULL        |                |
| q4          | varchar(255) | NO       |         | NULL        |                |
| q5          | varchar(255) | NO       |         | NULL        |                |
| q6          | varchar(255) | NO       |         | NULL        |                |
| q7          | varchar(255) | NO       |         | NULL        |                |
| q8          | varchar(255) | NO       |         | NULL        |                |
| q9          | varchar(255) | NO       |         | NULL        |                |
| q10         | varchar(255) | NO       |         | NULL        |                |
| q11         | varchar(255) | NO       |         | NULL        |                |
| q12         | varchar(255) | NO       |         | NULL        |                |
| q13         | varchar(255) | NO       |         | NULL        |                |
| q14         | varchar(255) | NO       |         | NULL        |                |
| q15         | varchar(255) | NO       |         | NULL        |                |
| q16         | varchar(255) | NO       |         | NULL        |                |
| q17         | varchar(255) | NO       |         | NULL        |                |
| q18         | varchar(255) | NO       |         | NULL        |                |
| q19         | varchar(255) | NO       |         | NULL        |                |
| q20         | varchar(255) | NO       |         | NULL        |                |
| q21         | varchar(255) | NO       |         | NULL        |                |
| q22         | varchar(255) | NO       |         | NULL        |                |
| q23         | varchar(255) | NO       |         | NULL        |                |
| q24         | varchar(255) | NO       |         | NULL        |                |

---
### Tabla: Interview_vendors

| **Field**    | **Type**    | **Null** | **Key** | **Default** | **Extra**      |
|-------------|--------------|----------|---------|-------------|----------------|
| id          | int          | NO       | PRI     | NULL        | auto_increment |
| id_location | int          | NO       | MUL     | NULL        |                |
| link        | varchar(500) | NO       |         | NULL        |                |
| q1          | varchar(255) | NO       |         | NULL        |                |
| q2          | varchar(255) | NO       |         | NULL        |                |
| q3          | varchar(255) | NO       |         | NULL        |                |
| q4          | varchar(255) | NO       |         | NULL        |                |
| q5          | varchar(255) | NO       |         | NULL        |                |
| q6          | varchar(255) | NO       |         | NULL        |                |
| q7          | varchar(255) | NO       |         | NULL        |                |
| q8          | varchar(255) | NO       |         | NULL        |                |
| q9          | varchar(255) | NO       |         | NULL        |                |
| q10         | varchar(255) | NO       |         | NULL        |                |
| q11         | varchar(255) | NO       |         | NULL        |                |
| q12         | varchar(255) | NO       |         | NULL        |                |
| q13         | varchar(255) | NO       |         | NULL        |                |
| q14         | varchar(255) | NO       |         | NULL        |                |
| q15         | varchar(255) | NO       |         | NULL        |                |
| q16         | varchar(255) | NO       |         | NULL        |                |
| q17         | varchar(255) | NO       |         | NULL        |                |
| q18         | varchar(255) | NO       |         | NULL        |                |
| q19         | varchar(255) | NO       |         | NULL        |                |
| q20         | varchar(255) | NO       |         | NULL        |                |
| q21         | varchar(255) | NO       |         | NULL        |                |
| q22         | varchar(255) | NO       |         | NULL        |                |
| q23         | varchar(255) | NO       |         | NULL        |                |

---

## Instalación

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/aldrinchp/Plants_system.git
   ```

2. **Instalar las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar la base de datos**:
   - Asegúrate de tener creado un tabla llamada Medicinal_plants_proyect en una instancia de MySQL.
   - Actualiza la configuración de la base de datos en el archivo `config.py` con tus credenciales de MySQL.

8. **Ejecutar la aplicación**:
   ```bash
   tu_directorio/app.py
   ```

---

## Uso

Una vez que la aplicación esté en funcionamiento, puedes interactuar con la API utilizando herramientas como [Postman](https://www.postman.com/) o [cURL](https://curl.se/).

### Endpoints Principales

#### Plants

- `POST /plants`: Crea una nuevo registro de una planta.
- `DELETE /plants/<id>`: Elimina un registro de una planta.
- `GET /plants/all_plants`: Obtiene la lista de todos las plantas registradas.
- `GET /plants/<id>`: Obtiene información de una planta específica.
- `PUT /plants/<id>`: Actualiza información de una planta.


#### Locations

- `POST /locations`: Crea un nuevo registro de un sitio.
- `DELETE /locations/<id>`: Elimina un registro de un sitio.
- `GET /locations/all_locations`: Obtiene la lista de todos los sitios.
- `GET /locations/<id>`: Obtiene información de un sitio específico.
- `PUT /locations/<id>`: Actualiza información de un sitio.

#### Images

- `POST /images`: Crea un nuevo registro de imagen.
- `DELETE /images/<id>`: Elimina un registro de imagen.
- `GET /images/all_images`: Obtiene la lista de todos los sitios.
- `GET /images/<id>`: Obtiene información de un sitio específico.
- `PUT /images/<id>`: Actualiza información de un sitio.
---
Los queries para las demas tablas pueden ser inferidos a partir de las inferencias anteriores.

## Contacto

Cualquier duda, puedes contactarme:

- **Nombre**: [Aldrin](https://github.com/aldrinchp)

- **Correo**: aldrinchp@gmail.com
