from flask import Blueprint, flash, redirect, render_template, request

from marvel_shop.forms import ProductForm 
from marvel_shop.models import Product, db

site = Blueprint('site', __name__, template_folder='app_templates' )


#use site object to create our routes
@site.route('/')
def index():
    allprods = Product.query.all() #the same as SELECT * FROM products, list of objects 
    print(allprods)
    return render_template('index.html', prods=allprods, prods_len = len(allprods))

@site.route('/products')
def products():
    allprods = Product.query.all() #the same as SELECT * FROM products, list of objects 
    print(allprods)
    return render_template('index.html', prods=allprods)

@site.route('/products/create',methods=['GET', 'POST'])
def create():
    createform = ProductForm()
    if request.method == 'POST' and createform.validate_on_submit():
        #grab our data from our form
        name = createform.name.data
        image = createform.image.data
        description = createform.description.data
        category = createform.category.data
        price = createform.price.data
        quantity = createform.quantity.data 

        #instantiate that class as an object passing in our arguments to replace our parameters 
        
        product = Product(name, price, quantity, category, image, description)

        db.session.add(product) #adding our new instantiating object to our database
        db.session.commit()

        flash(f"You have successfully created product {name}", category='success')
        return redirect('/')
    
    elif request.method == 'POST':
        flash("We were unable to process your request", category='warning')
        return redirect('/shop/create')
    return render_template('create.html', form=createform)

@site.route('/products/<id>',methods=['GET', 'POST'])
def update(id):
        #lets grab our specific product we want to update
    product = Product.query.get(id)     # this should only ever bring back 1 item/object
    updateform = ProductForm()
    return render_template('create.html', form=updateform, product=product, is_update=True )

@site.route('/products/delete/<id>')
def delete(id):

    #query our database to find that object we want to delete
    product = Product.query.get(id)

    db.session.delete(product)
    db.session.commit()

    return redirect('/')