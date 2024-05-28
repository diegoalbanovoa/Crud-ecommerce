from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config.Config')
db = SQLAlchemy(app)

# Import models
from models import Product

# Crear la base de datos
@app.before_first_request
def create_tables():
    db.create_all()

# Ruta para obtener todos los productos
@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([product.as_dict() for product in products])

# Ruta para obtener un producto por ID
@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    if product is None:
        abort(404)
    return jsonify(product.as_dict())

# Ruta para crear un nuevo producto
@app.route('/products', methods=['POST'])
def create_product():
    if not request.json or not 'name' in request.json:
        abort(400)
    new_product = Product(
        name=request.json['name'],
        price=request.json.get('price', 0.0),
        description=request.json.get('description', '')
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify(new_product.as_dict()), 201

# Ruta para actualizar un producto existente
@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)
    if product is None:
        abort(404)
    if not request.json:
        abort(400)
    product.name = request.json.get('name', product.name)
    product.price = request.json.get('price', product.price)
    product.description = request.json.get('description', product.description)
    db.session.commit()
    return jsonify(product.as_dict())

# Ruta para eliminar un producto
@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    if product is None:
        abort(404)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'result': True})

# Método para convertir un objeto Product a diccionario
def product_to_dict(product):
    return {
        'id': product.id,
        'name': product.name,
        'price': product.price,
        'description': product.description
    }

# Agregar método as_dict a la clase Product
Product.as_dict = product_to_dict

if __name__ == '__main__':
    app.run(debug=True)
