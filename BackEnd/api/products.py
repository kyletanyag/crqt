
'''
@author Alex Soliza, Kyle Tanyag
@brief this file contains processes to communicate with products db. 

'''

from flask import Blueprint, jsonify
from sqlalchemy import func
from .data_models import Products

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
def query_by_type(input):
    filter = Products.query.filter(func.lower(Products.type) == func.lower(input))
    results = []

    for i in filter:
        results.append({
            'vendor': i.vendor,
            'type': i.type,
            'product': i.product})

    if results:
        return jsonify({'query': results}), 200

    return {'error': f'Cannot query by the type: {input}'}, 200


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


