from werkzeug.security import generate_password_hash #generates a unique password hash for extra security 
from flask_sqlalchemy import SQLAlchemy #this is our ORM (Object Relational Mapper)
from flask_login import UserMixin, LoginManager #helping us load a user as our current_user 
from datetime import datetime #put a timestamp on any data we create (Users, Products, etc)
import uuid #makes a unique id for our data (primary key)
from flask_marshmallow import Marshmallow





#instantiate all our classes
db = SQLAlchemy() #make database object
login_manager = LoginManager() #makes login object 
ma = Marshmallow() #makes marshmallow object 


#use login_manager object to create a user_loader function
@login_manager.user_loader
def load_user(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (email) user to retrieve

    """
    return User.query.get(user_id) #this is a basic query inside our database to bring back a specific User object

#think of these as admin (keeping track of what products are available to sell)
class User(db.Model, UserMixin): 
    #CREATE TABLE User, all the columns we create
    user_id = db.Column(db.String, primary_key=True) 
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow) #this is going to grab a timestamp as soon as a User object is instantiated
    

    #INSERT INTO User() Values()
    def __init__(self, email, password, first_name="", last_name=""):
        self.user_id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email 
        self.password = self.set_password(password) 



    #methods for editting our attributes 
    def set_id(self):
        return str(uuid.uuid4()) #all this is doing is creating a unique identification token
    

    def get_id(self):
        return str(self.user_id) #UserMixin using this method to grab the user_id on the object logged in
    
    
    def set_password(self, password):
        return generate_password_hash(password) #hashes the password so it is secure (aka no one can see it)
    

    def __repr__(self):
        return f"<User: {self.email}>"
    

class Product(db.Model):
    product_id = db.Column(db.String, primary_key=True) 
    name = db.Column(db.String)
    price = db.Column(db.Double)
    quantity = db.Column(db.Integer)
    category = db.Column(db.String)
    img = db.Column(db.String)
    description = db.Column(db.String)

    def __init__(self, name, price, quantity = 0, category = "", img= "", description = ""):
        self.product_id = self.set_id()
        self.name = name
        self.price = price
        self.quantity = quantity
        self.category = category
        self.img = img
        self.description = description

        
    #methods for editting our attributes 
    def set_id(self):
        return str(uuid.uuid4()) #all this is doing is creating a unique identification token
    

    def get_id(self):
        return str(self.product_id) #UserMixin using this method to grab the user_id on the object logged in
    
    def __repr__(self):
        return f"<Product: {self.name}>"    

class ProdOrder(db.Model):
    prod_order_id =  db.Column(db.String, primary_key=True) 
    order_id = db.Column(db.String, db.ForeignKey('order.order_id'), nullable = False)
    product_id = db.Column(db.String, db.ForeignKey('product.product_id'), nullable = False)
    price = db.Column(db.Double, nullable = False)
    quantity = db.Column(db.Integer, nullable = False)

    def __init__(self, order_id, product_id, price, quantity=0):
        self.prod_order_id = self.set_id()
        self.order_id = order_id
        self.product_id = product_id
        self.price = price
        self.quantity = quantity

        #methods for editting our attributes 
    def set_id(self):
        return str(uuid.uuid4()) #all this is doing is creating a unique identification token
    
class Order(db.Model):
    order_id = db.Column(db.String, primary_key=True) 
    customer_id = db.Column(db.String, db.ForeignKey('customer.cust_id'), nullable = False)
    products = db.relationship('ProdOrder', backref = 'order', lazy=True) 

    def __init__(self, customer_id):
        self.order_id = self.set_id()
        self.customer_id = customer_id

    def set_id(self):
        return str(uuid.uuid4()) #all this is doing is creating a unique identification token

class Customer(db.Model):
    cust_id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    email = db.Column(db.String(30))
    orders = db.relationship('Order', backref = 'customer', lazy=True)
    date_created = db.Column(db.String, default = datetime.utcnow() )

    
    def __init__(self, first_name, last_name, email):
        self.cust_id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
    
        #methods for editting our attributes 
    def set_id(self):
        return str(uuid.uuid4()) #all this is doing is creating a unique identification token
    

    def __repr__(self):
        return f"<Customer: {self.first_name}>"
    

# creating our Schema class (Schema essentially just means what our data "looks" like, and our 
# data needs to look like a dictionary (json) not an object)


class ProductSchema(ma.Schema): # dto Data transfer object

    class Meta:
        fields = ['product_id', 'name', 'img', 'description', 'price', 'quantity']



#instantiate our ProductSchema class so we can use them in our application
product_schema = ProductSchema() #this is 1 singular product
products_schema = ProductSchema(many=True) #bringing back all the products in our database & sending to frontend

class CustomerSchema(ma.Schema): # dto Data transfer object

    class Meta:
        fields = ['cust_id', 'first_name', 'last_name', 'email']

#instantiate our ProductSchema class so we can use them in our application
customer_schema = CustomerSchema() #this is 1 singular product
customers_schema = CustomerSchema(many=True) #bringing back all the products in our database & sending to frontend


    