from flask import Blueprint, render_template,request,flash
from flask_login import current_user
from .models import *

views=Blueprint('views',__name__)

@views.route('/')
@views.route('/home')
def home():
    return render_template('home.html',user=current_user)

@views.route('/clothes')
def clothes():
    page=request.args.get('page',1,type=int)
    sort=request.args.get('sort','oldest',type=str)
    productType='clothes'
    filteredProducts=getFilteredProducts(productType)
    sortedFilteredProducts=getSortedProducts(sort,page,filteredProducts)
    return render_template('clothes.html',user=current_user,products=sortedFilteredProducts)

@views.route('/perfumes')
def perfumes():
    page=request.args.get('page',1,type=int)
    sort=request.args.get('sort','oldest',type=str)
    productType='perfumes'
    filteredProducts=getFilteredProducts(productType)
    sortedFilteredProducts=getSortedProducts(sort,page,filteredProducts)
    return render_template('perfumes.html',user=current_user,products=sortedFilteredProducts)

@views.route('/handbags')
def handbags():
    page=request.args.get('page',1,type=int)
    sort=request.args.get('sort','oldest',type=str)
    productType='handbags'
    filteredProducts=getFilteredProducts(productType)
    sortedFilteredProducts=getSortedProducts(sort,page,filteredProducts)
    return render_template('handbags.html',user=current_user,products=sortedFilteredProducts)

@views.route('/viewProduct')
def viewProduct():
    productId=request.args.get('id',1,type=int)
    currentColor=request.args.get('color','none',type=str)
    product=Product.query.join(Product.product_configs).filter(Product.id==productId).first()
    availableColors=[]
    if product.type=='clothes':
        for config in product.product_configs:
            if config.quantity>0:
                if config.color not in availableColors:
                    availableColors.append(config.color)
    return render_template('viewProduct.html',user=current_user,product=product,currentColor=currentColor,availableColors=availableColors)

def getSortedProducts(sort,page,products):
    if sort=='oldest':
        sortedProducts=products.order_by(Product.id.asc()).paginate(page=page,per_page=8)
    elif sort=='newest':
        sortedProducts=products.order_by(Product.id.desc()).paginate(page=page,per_page=8)
    elif sort=='price-low-high':
        sortedProducts=products.order_by(Product.price.asc()).paginate(page=page,per_page=8)
    elif sort=='price-high-low':
        sortedProducts=products.order_by(Product.price.desc()).paginate(page=page,per_page=8)

    return sortedProducts

def getFilteredProducts(productType):
    if productType=='clothes':
        filterSizes=getFilterSizes()
        filteredProducts=Product.query.filter(Product.type==productType,Product.product_configs.any(Product_config.size.in_(filterSizes)),Product.product_configs.any(Product_config.quantity>0))
    if productType=='perfumes':
        filteredProducts=Product.query.filter(Product.type==productType,Product.product_configs.any(Product_config.quantity>0))
    if productType=='handbags':
        filteredProducts=Product.query.filter(Product.type==productType,Product.product_configs.any(Product_config.quantity>0))
    
    return filteredProducts

def getFilterSizes():
    filterSizes=[]
    if request.args.get('xs','false',type=str)=='true':
        filterSizes.append('xs')
    if request.args.get('s','false',type=str)=='true':
        filterSizes.append('s')
    if request.args.get('m','false',type=str)=='true':
        filterSizes.append('m')
    if request.args.get('l','false',type=str)=='true':
        filterSizes.append('l')
    if request.args.get('xl','false',type=str)=='true':
        filterSizes.append('xl')
    if filterSizes==[]:
        filterSizes=['xs','s','m','l','xl']
    return filterSizes
