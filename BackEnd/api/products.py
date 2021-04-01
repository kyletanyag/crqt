
'''
@author Alex Soliza, Kyle Tanyag
@brief this file contains processes to communicate with products db. 

'''

from flask import Blueprint, jsonify, request
from sqlalchemy import func
from sqlalchemy.sql.expression import false, null, true
from .data_models import Products
from . import products

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


# query with Products database to get vendor products by product type
@product_bp.route('/product_query_by_type/<input_type>', methods=['GET'])
def query_by_type(input_type):
    filter = Products.query.filter(func.lower(Products.type) == func.lower(input_type))
    results = []

    for i in filter:
        results.append({
            'vendor': i.vendor,
            'type': i.type,
            'product': i.product})

    if results:
        return jsonify({'query': results}), 200

    return {'error': f'Cannot query by the type: {input_type}'}, 200


# query with Products database to get vendor products by product name
@product_bp.route('/product_query/<input_type>/<input_vendor>', methods=['GET'])
def query_by_product(input_type, input_vendor):
    filter = Products.query.filter(func.lower(Products.type) == func.lower(input_type), func.lower(Products.vendor) == func.lower(input_vendor))
    results = []

    for i in filter:
        results.append({
            'vendor': i.vendor,
            'type': i.type,
            'product': i.product})

    if results:
        return jsonify({'query': results}), 200
    
    return {'error': f'Cannot query by the type: {input_type} and vendor: {input_vendor}'}, 200

# json object is recieved from front-end, parsed, and new product is added to db
@product_bp.route('/product_add', methods=['POST'])
def product_add():
    incoming_data = request.get_json() # product info: vendor, type, product

    new_product = Products(
        vendor = incoming_data['vendor'],
        type = incoming_data['type'],
        product = incoming_data['product'])

    if (check_products_for_duplicate(new_product.vendor, new_product.type, new_product.product)):
        products.session.add(new_product)
        products.session.commit()
        
        return 'Done', 201

# checks for a duplicate in the products db. returns true if a duplicate is found
def check_products_for_duplicate(input_vendor, input_type, input_product):
    prod_search= Products.query.filter(
        vendor=input_vendor,
        type=input_type,
        product=input_product).first()
    
    return not (prod_search is None)