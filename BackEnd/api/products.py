
'''
@author Alex Soliza, Kyle Tanyag
@brief this file contains processes to communicate with products db. 

'''

from flask import Blueprint, jsonify, request
from sqlalchemy import func
from sqlalchemy.sql.expression import false, null, true
from .data_models import Products
from . import products
from . import db 

product_bp = Blueprint('product_bp', __name__)

# query with Products database to get vendor products by vendor name
@product_bp.route('/product_query_by_vendor/<input>', methods=['GET'])
def query_by_vendor(input):
    filter = Products.query.filter(func.lower(Products.vendor) == func.lower(input))
    results = []

    for i in filter:
        results.append({
            'vendor': i.vendor,
            'type': i.type,
            'product': i.product})

    if results:
        return jsonify({'query': results}), 200
    
    return {'error': f'Cannot query by the vendor: {input}'}, 200

@product_bp.route('/get_all_products', methods=['GET'])
def get_all():
    query = db.session.query(Products.vendor, Products.product, Products.type, ).distinct(Products.vendor)    
    results = []

    for i in query:
        results.append({
            'vendor': i.vendor,
            'product': i.product,
            'type': i.type
        })

    if results:
        return jsonify({'query': results}), 200

    return {'error': 'Cannot execute query'}, 200   

# query with Products database to get vendor products by product type
@product_bp.route('/product_query_by_type/<input_type>', methods=['GET'])
def query_by_type(input_type):
    query = db.session.query(Products.vendor, Products.type).filter(func.lower(Products.type) == func.lower(input_type)).distinct(Products.vendor)
    results = []

    for i in query:
        results.append(i.vendor)

    if results:
        return jsonify({'query': results}), 200

    return {'error': f'Cannot query by the type: {input_type}'}, 200


# query with Products database to get vendor products by product name
@product_bp.route('/product_query/<input_type>/<input_vendor>', methods=['GET'])
def query_by_product(input_type, input_vendor):
    filter = Products.query.filter(func.lower(Products.type) == func.lower(input_type), func.lower(Products.vendor) == func.lower(input_vendor)).order_by(Products.product)
    results = []

    for i in filter:
        results.append(i.product)

    if results:
        return jsonify({'query': results}), 200
    
    return {'error': f'Cannot query by the type: {input_type} and vendor: {input_vendor}'}, 200


@product_bp.route('/product_remove/<input_vendor>/<input_product>/<input_type>')
def product_remove(input_vendor, input_product, input_type):
    product = Products.query.filter(
        func.lower(Products.vendor) == func.lower(input_vendor),
        func.lower(Products.type) == func.lower(input_type),
        func.lower(Products.product) == func.lower(input_product)).first()

    db.session.delete(product)
    db.session.commit()

    return 'Done', 200    


# json object is recieved from front-end, parsed, and new product is added to db
@product_bp.route('/product_add', methods=['POST'])
def product_add():
    incoming_data = request.get_json() # product info: vendor, type, product

    new_product = Products(
        vendor = incoming_data['vendor'],
        type = incoming_data['type'],
        product = incoming_data['product'])

    if (check_products_for_duplicate(incoming_data['vendor'], incoming_data['type'], incoming_data['product'])):
        db.session.add(new_product)
        db.session.commit()
        
        return {'status': 'Product Added!'}, 201

    else:
        return {'error': 'Duplicate entry. Cannot add product.'}, 201

# checks for a duplicate in the products db. returns true if a duplicate is found
def check_products_for_duplicate(input_vendor, input_type, input_product):
    prod_search = Products.query.filter(
        func.lower(Products.vendor) == func.lower(input_vendor),
        func.lower(Products.type) == func.lower(input_type),
        func.lower(Products.product) == func.lower(input_product)).first()
    
    return True if prod_search is None else False