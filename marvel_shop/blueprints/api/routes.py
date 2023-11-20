from flask import Blueprint, request, jsonify, Response
from flask_jwt_extended import create_access_token, jwt_required 
from marvel_shop.models import Customer, Product, ProdOrder, Order, db, product_schema, products_schema, customer_schema, customers_schema



api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/token', methods = ['GET', 'POST'])
def token():
    data = request.json
    if data:
        client_id = data['client_id']
        access_token = create_access_token(identity=client_id) # just needs a unique identifier 
        return {
            'status': 200,
            'access_token': access_token
        }
    else:
        return {
            'status' : 400,
            'message' : 'Missing Client Id. Try Again.'
        }

@api.get('/products') # @api.route('/products', methods = [GET])
@jwt_required()
def get_products():

    # this is a list of objects
    allprods = Product.query.all()

    # since we cant send a list of objects through api calls we need to change them into dictionaries/jsonify them
    response = products_schema.dump(allprods) # loop through allprods list of objects and change objects into dictionarys
    return jsonify(response)

@api.route('/customer', methods = ['POST']) #CREATE is usually paired with a POST method 
@jwt_required()
def create_customer():
    data =  request.json
    customer = data["customer"]
    if Customer.query.filter(Customer.email == customer['email']).first(): 
        return {
            'message' : 'This email is already in use'
        }, 409
    new_customer = Customer(customer['first_name'], customer['last_name'], customer['email'])
    db.session.add(new_customer)
    db.session.commit()
    return {
        'status': 200,
        'customer': customer_schema.dump(new_customer)
    }, 200

@api.route('/customer', methods = ['GET']) #CREATE is usually paired with a POST method 
@jwt_required()
def list_customer():
    allcustomers = Customer.query.all()
        
    return {
        'customers': customers_schema.dump(allcustomers)
    }, 200

@api.get('customer/<id>')
@jwt_required()
def get_customer(id):
    customer = Customer.query.get(id)
    if not customer:
        return {
            "message" : "Customer does not exist"
        }, 404
    return {
        'customer': customer_schema.dump(customer)
    }, 200

@api.get('customer/<id>/orders')
@jwt_required()
def get_customer_orders(id):
    customer = Customer.query.get(id)
    if not customer:
        return {
            "message" : "Customer does not exist"
        }, 404
    data = []
    for order in customer.orders:
        order_dict = {
            "order_id": order.order_id,
            "products": products_schema.dump(order.products)
                      }
        data.append(order_dict)
    return {
        'customer': customer_schema.dump(customer),
        'orders': data
    }, 200


@api.route('/order', methods=['POST'])
@jwt_required()
def create_order():
    data =  request.json
    customer_id = data["customer_id"]
    customer = Customer.query.filter(Customer.cust_id == customer_id).first()
    if not customer:
        return {
            "message" : "Customer does not exist"
        }, 404
    order = Order(customer_id=customer_id)
    db.session.add(order)
    db.session.commit()
    return {
        "message" : "Order created with success",
        "order" : order.order_id
    }, 200

@api.post('/order/<id>/add_product')
@jwt_required()
def add_product(id):
    data =  request.json
    product_id = data["product_id"]
    quantity = data["quantity"]

    order = Order.query.get(id)
    if not order:
        return {
            "message" : "Order does not exist"
        }, 404
    product = Product.query.get(product_id)
    if not product:
        return {
            "message" : "Product does not exist"
        }, 404
    
    prodorder = ProdOrder.query.filter(ProdOrder.order_id == id, ProdOrder.product_id == product_id).first()
   
    if not prodorder:
        prodorder = ProdOrder(id,  product.product_id, product.price,quantity )
        db.session.add(prodorder)
    else:
        prodorder.quantity = prodorder.quantity + quantity
    db.session.commit()

    db.session.refresh(order)
    return {
        "order_id": id,
        "products": products_schema.dump(order.products)
    },200

@api.post('/order/<id>/remove_product')
@jwt_required()
def remove_product(id):
    data =  request.json
    product_id = data["product_id"]
    quantity = data["quantity"]
    order = Order.query.get(id)
    if not order:
        return {
            "message" : "Order does not exist"
        }, 404
    
    prodorder = ProdOrder.query.filter(ProdOrder.order_id == id, ProdOrder.product_id == product_id).first()
    if not prodorder:
        return {
            "message" : "Product is not on the Order"
        }, 404\
    
    prodorder.quantity = prodorder.quantity - quantity
    if  prodorder.quantity<1 :
        db.session.delete(prodorder)
    db.session.commit()
    
    db.session.refresh(order)
    return {
        "order_id": id,
        "products": products_schema.dump(order.products)
    },200

@api.get('/order/<id>')
@jwt_required()
def get_order(id):
    data =  request.json
    order = Order.query.get(id)
    if not order:
        return {
            "message" : "Order does not exist"
        }, 404
    
    return {
        "order_id": id,
        "products": products_schema.dump(order.products)
    },200


@api.route('/order/<id>/delete', methods=['POST'])
@jwt_required()
def delete_order(id):
    order = Order.query.get(id)
    if not order:
        return {
            "message" : "Order does not exist"
        }, 404
    db.session.delete(order)
    db.session.commit()
    return {
        "message": f'The order {id} was successfully deleted',
    
    },200

