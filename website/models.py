from . import database,login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

product_configuration=database.Table('product_configuration',
    database.Column('product_item_id',database.Integer, database.ForeignKey('product_item.id')),
    database.Column('variation_option_id',database.Integer, database.ForeignKey('variation_option.id'))
)

class User(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    email = database.Column(database.String(150), unique=True, nullable=False)
    password = database.Column(database.String(150), nullable=False)
    name = database.Column(database.String(150), nullable=False)
    phone = database.Column(database.String(12), nullable=False)
    date_registered = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    email_confirmed = database.Column(database.Boolean(), nullable=False, default=False)
    email_confirm_date = database.Column(database.DateTime)
    cart = database.relationship('Shopping_cart', backref='user', uselist=False)
    shop_orders=database.relationship('Shop_order',backref='user')

class User_address(database.Model):
    id=database.Column(database.Integer, primary_key=True)
    user_id=database.Column(database.Integer, database.ForeignKey('user.id'))
    address_id=database.Column(database.Integer, database.ForeignKey('address.id'))
    is_default=database.Column(database.Boolean(),default=False)

class Address(database.Model):
    id=database.Column(database.Integer, primary_key=True)
    country_id=database.Column(database.Integer, database.ForeignKey('country.id'))
    region=database.Column(database.String(150),nullable=False)
    city=database.Column(database.String(150),nullable=False)
    postal_code=database.Column(database.Integer,nullable=False)
    street_name=database.Column(database.String(150),nullable=False)
    house_number=database.Column(database.Integer, nullable=False)
    flat_number=database.Column(database.Integer)

class Country(database.Model):
    id=database.Column(database.Integer, primary_key=True)
    country=database.Column(database.String(150), nullable=False)

class User_payment_method(database.Model):
    id=database.Column(database.Integer, primary_key=True)
    user_id=database.Column(database.Integer, database.ForeignKey('user.id'))
    payment_type_id=database.Column(database.Integer, database.ForeignKey('payment_type.id'))
    provider=database.Column(database.String(150),nullable=False)
    account_number=database.Column(database.Integer, nullable=False)
    expiry_date=database.Column(database.DateTime,nullable=False)
    is_default=database.Column(database.Boolean(), default=False)

class Payment_type(database.Model):
    id=database.Column(database.Integer, primary_key=True)
    value=database.Column(database.String(150),nullable=False)    

class Shopping_cart(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    user_id=database.Column(database.Integer, database.ForeignKey('user.id'), unique=True)
    shopping_cart_items=database.relationship('Shopping_cart_item', backref='shopping_cart')

class Shopping_cart_item(database.Model):
    id=database.Column(database.Integer, primary_key=True)
    shopping_cart_id=database.Column(database.Integer, database.ForeignKey('shopping_cart.id'))
    product_item_id=database.Column(database.Integer,database.ForeignKey('product_item.id'))
    quantity=database.Column(database.Integer, nullable=False)

class Product(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(150), nullable=False)
    description = database.Column(database.String(300), nullable=False)
    image_url = database.Column(database.String(150), nullable=False)
    category_id = database.Column(database.Integer, database.ForeignKey('product_category.id'))
    product_items=database.relationship('Product_item', backref='product')

class Product_item(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    product_id=database.Column(database.Integer, database.ForeignKey('product.id'))
    images = database.relationship('product_image', backref='product_item')
    variation=database.relationship('Variation_option' , secondary=product_configuration)
    sku=database.Column(database.String(150), unique=True)
    price = database.Column(database.Integer, nullable=False)
    quantity_in_stock = database.Column(database.Integer)

class Product_category(database.Model):
    id=database.Column(database.Integer, primary_key=True)
    category_name=database.Column(database.String(150), nullable=False)

class Product_image(database.Model):
    id=database.Column(database.Integer, primary_key=True)
    product_item_id=database.Column(database.Integer,database.ForeignKey('product_item.id'))
    image_url=database.Column(database.String(150),nullable=False)

class Variation(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    category_id=database.Column(database.Integer, database.ForeignKey('product_category.id'))
    name=database.Column(database.String(150), nullable=False)

class Variation_option(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    variation_id=database.Column(database.Integer, database.ForeignKey('variation.id'))
    value=database.Column(database.String(150), nullable=False)

class Shop_order(database.Model):
    id=database.Column(database.Integer, primary_key=True)
    user_id=database.Column(database.Integer, database.ForeignKey('user.id'))
    order_date = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    payment_method_id=database.Column(database.Integer, database.ForeignKey('user_payment_method.id'))
    shipping_address_id=database.Column(database.Integer, database.ForeignKey('address.id'))
    shipping_method_id=database.Column(database.Integer, database.ForeignKey('shipping_method.id'))
    order_total=database.Column(database.Integer, nullable=False)
    order_products=database.relationship('Order_line')
    order_status=database.Column(database.Integer, database.ForeignKey('order_status.id'))

class Shipping_method(database.Model):
    id=database.Column(database.Integer,primary_key=True)
    name=database.Column(database.String(150),nullable=False)
    price=database.Column(database.Integer,nullable=False)

class Order_status(database.Model):
    id=database.Column(database.Integer, primary_key=True)
    status=database.Column(database.String(150), nullable=False)

class Order_line(database.Model):
    id=database.Column(database.Integer, primary_key=True)
    product_item_id=database.Column(database.Integer, database.ForeignKey('product_item.id'))
    order_id=database.Column(database.Integer, database.ForeignKey('shop_order.id'))
    quantity=database.Column(database.Integer,nullable=False)
    price=database.Column(database.Integer, nullable=False)

class User_review(database.Model):
    id=database.Column(database.Integer,primary_key=True)
    user_id=database.Column(database.Integer, database.ForeignKey('user.id'))
    ordered_product_id=database.Column(database.Integer, database.ForeignKey('order_line.id'))
    rating_value=database.Column(database.Integer)
    comment=database.Column(database.String(150))
