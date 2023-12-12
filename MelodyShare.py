from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

app = Flask(__name__)

app.config['SECRET_KEY']='dsfcsdvsdv'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://msctrl:abcd1234@localhost:3306/melodyshare'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Model Design and linking Database

class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True,unique=True)
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
    address = db.Column(db.String(255))
    mobile = db.Column(db.String(11))
    Fname = db.Column(db.String(255))
    Lname = db.Column(db.String(255))
    aType = db.Column(db.String(255))
    #notes = db.relationship('Note')


    def __repr__(self) -> str:
        return f'{self.id} - {self.email} - {self.username}'
    
class Products(UserMixin, db.Model):

    pid = db.Column(db.Integer, primary_key=True,unique=True,autoincrement=True)
    pname = db.Column(db.String(100))
    pprice = db.Column(db.Integer)
    ptype = db.Column(db.String(100))
    pimage = db.Column(db.String(100))
    pdescription = db.Column(db.String(255))
    powner = db.Column(db.String(100))
    pownerid = db.Column(db.Integer)
    pc = db.Column(db.String(100))
    
    def __repr__(self) -> str:
        return f'{self.pid} - {self.pname} - {self.pprice} - {self.ptype} - {self.pimage} - {self.pdescription} - {self.powner} - {self.pownerid}'
    
class Products2(UserMixin, db.Model):

    p_id = db.Column(db.Integer, primary_key=True,unique=True,autoincrement=True)
    p_name = db.Column(db.String(100))
    p_price = db.Column(db.Integer)
    p_type = db.Column(db.String(100))
    p_area = db.Column(db.String(100))
    p_description = db.Column(db.String(255))
    p_owner = db.Column(db.String(100))
    p_ownerid = db.Column(db.Integer)
    
    def __repr__(self) -> str:
        return f'{self.p_id} - {self.p_name} - {self.p_price} - {self.p_type} - {self.p_description} - {self.p_owner} - {self.p_ownerid} - {self.p_area}'
    
class Cart(UserMixin, db.Model):
    
        c_id = db.Column(db.Integer, primary_key=True,unique=True,autoincrement=True)
        c_p_id = db.Column(db.Integer)
        c_p_name = db.Column(db.String(100))
        c_p_price = db.Column(db.Integer)
        cptype = db.Column(db.String(100))
        cpimage = db.Column(db.String(100))
        cpdescription = db.Column(db.String(255))
        cpowner = db.Column(db.String(100))
        c_userid = db.Column(db.Integer)
        cowner = db.Column(db.String(100))
        cownerid = db.Column(db.Integer)
        
        def __repr__(self) -> str:
            return f'{self.c_id} - {self.c_p_id} - {self.c_p_name} - {self.c_p_price} - {self.cptype} - {self.cpimage} - {self.cpdescription} - {self.cpowner} - {self.c_userid} - {self.cowner} - {self.cownerid}'



class Order(UserMixin, db.Model):
    
        o_id = db.Column(db.Integer, primary_key=True,unique=True,autoincrement=True)
        o_username = db.Column(db.String(100))
        o_userid = db.Column(db.Integer)
        o_email = db.Column(db.String(100))
        o_address = db.Column(db.String(255))
        o_mobile = db.Column(db.String(11))
        o_method = db.Column(db.String(100))
        o_total = db.Column(db.Integer)
        o_status = db.Column(db.String(100))
        o_bkash = db.Column(db.String(100))
        o_trxid = db.Column(db.String(100))
        p_ownerid = db.Column(db.String(100))
        cart_id = db.Column(db.String(100))


# !!! Model Design and linking Database


login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user):
    return User.query.get(int(user))

# Route Structures 

@app.route('/')
def index():
    return render_template('landing.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('useremail')
        username = request.form.get('username')
        password = request.form.get('userpassword')
        aType = request.form.get('aType')
        print(aType)
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(password, method='sha256'),aType = aType)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        
    return render_template("signup.html", user=current_user)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('useremail')
        password = request.form.get('userpassword')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully.', category='success')
                login_user(user, remember=True)
                print(current_user)
                
                return redirect(url_for('profiles',id = current_user.id))
            else:
                flash('Incorrect password, try again.', category='error')
                return redirect(url_for('register'))
        else:
            flash('Email does not exist.', category='error')
    return render_template("signin.html", user=current_user)

@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/delac")
@login_required
def delAc():
    
    user = current_user.query.filter_by(id=current_user.id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('login'))

@app.route("/profiles/<int:id>", methods=['GET', 'POST'])
@login_required
def profiles(id):
    if request.method == 'POST':
        
        user = current_user.query.filter_by(id=current_user.id).first()
        id = user.id
        Fname = request.form.get('Fname')
        user.Fname = Fname
        Lname = request.form.get('Lname')
        user.Lname = Lname
        mobile = request.form.get('mobile')
        user.mobile = mobile
        address = request.form.get('address')
        user.address = address
        db.session.commit()
        return render_template("profile.html",user=current_user,id=id)
    
    id = id
    user1 = current_user.query.filter_by(id=id).first()
    return render_template("profile.html", user=current_user,id = id,user1=user1)


@app.route("/products", methods=['GET', 'POST'])
@login_required
def products():
    user = current_user.query.filter_by(id=current_user.id).first()
    prods = Products.query.filter_by(pownerid=user.id).all()
    Aprods = Products.query.all()
    return render_template("Products.html",user=current_user, prods=prods, Aprods=Aprods)

@app.route("/products2", methods=['GET', 'POST'])
@login_required
def products2():
    user = current_user.query.filter_by(id=current_user.id).first()
    prods = Products2.query.filter_by(p_ownerid=user.id).all()
    Aprods = Products2.query.all()
    return render_template("Products2.html",user=current_user, prods=prods, Aprods=Aprods)

@app.route("/AddProduct", methods=['GET', 'POST'])
@login_required
def AddProduct():
    if request.method == 'POST':
            user = current_user.query.filter_by(id=current_user.id).first()
            uid = user.id
            uname = user.username
            product = Products.query.filter_by(pid=Products.pid).first()
            pname = request.form.get('pname')

            pprice = request.form.get('pprice')
            pc = request.form.get('pc')

            ptype = request.form.get('ptype')

  
            pdescription = request.form.get('pdescription')
            #image = request.files['pimage']

            
            
            new_product = Products(pname=pname, pprice=pprice, ptype=ptype, pdescription=pdescription, powner=uname, pownerid=uid,pc=pc)
            db.session.add(new_product)
            db.session.commit()
            return redirect(url_for('products'))
    return render_template("AddProduct.html",user=current_user)

@app.route("/AddProduct2", methods=['GET', 'POST'])
@login_required
def AddProduct2():
    if request.method == 'POST':
            user = current_user.query.filter_by(id=current_user.id).first()
            uid = user.id
            uname = user.username
            product = Products2.query.filter_by(p_id=Products2.p_id).first()
            p_name = request.form.get('pname')

            p_price = request.form.get('pprice')

            p_type = request.form.get('ptype')
            p_area = request.form.get('parea')
  
            p_description = request.form.get('pdescription')


            
            
            new_product = Products2(p_name=p_name, p_price=p_price, p_type=p_type, p_description=p_description, p_owner=uname, p_ownerid=uid, p_area=p_area)
            db.session.add(new_product)
            db.session.commit()
            return redirect(url_for('products2'))
    return render_template("AddProduct2.html",user=current_user)
    
@app.route("/delAProd/<int:pid>")
@login_required
def delAProd(pid):
    prod = Products.query.filter_by(pid=pid).first()
    db.session.delete(prod)
    db.session.commit()
    return redirect(url_for('products'))

@app.route("/delAProd2/<int:p_id>")
@login_required
def delAProd2(p_id):
    prod = Products2.query.filter_by(p_id=p_id).first()
    db.session.delete(prod)
    db.session.commit()
    return redirect(url_for('products2'))
    
@app.route("/productDetails/<int:pid>",methods=['GET', 'POST'])
@login_required
def productDetails(pid):
    prod = Products.query.filter_by(pid=pid).first()
    user = current_user.query.filter_by(id=current_user.id).first()
    cartitems = Cart.query.filter_by(c_userid=user.id).count()
    print(cartitems)
    return render_template('productDetails.html',user=user, prod=prod, cartitems=cartitems)

@app.route("/productDetails2/<int:pid>",methods=['GET', 'POST'])
@login_required
def productDetails2(pid):
    prod = Products2.query.filter_by(p_id=pid).first()
    user = current_user.query.filter_by(id=current_user.id).first()
    return render_template('productDetails.html',user=user, prod=prod)

@app.route("/cart",methods=['GET', 'POST'])
@login_required
def cart():
    user = current_user.query.filter_by(id=current_user.id).first()
    cart = Cart.query.filter_by(c_userid=user.id).all()
    cartitems = Cart.query.filter_by(c_userid=user.id).count()
    ct = 0
    for i in cart:
        ctotal = (i.c_p_price)
        ct = ct + ctotal

    return render_template('cart.html',user=user, cart=cart, cartitems=cartitems, ctotal=ct)

@app.route("/addtocart/<int:p_id>",methods=['GET', 'POST'])
@login_required
def addtocart(p_id):
    prod = Products.query.filter_by(pid=p_id).first()
    user = current_user.query.filter_by(id=current_user.id).first()
    uid = user.id
    uname = user.username
    cowner = prod.powner
    cownerid = prod.pownerid
    c_p_id = prod.pid
    c_p_name = prod.pname
    c_p_price = prod.pprice
    cptype = prod.ptype
    #cpimage = prod.pimage
    cpdescription = prod.pdescription
    c_userid = user.id
    new_cart = Cart(c_p_id=c_p_id, c_p_name=c_p_name, c_p_price=c_p_price, cptype=cptype, cpdescription=cpdescription, cpowner=cowner, c_userid=c_userid, cowner=cowner, cownerid=cownerid)
    db.session.add(new_cart)
    db.session.commit()
    return redirect(url_for('cart'))

@app.route("/delcart/<int:c_id>")
@login_required
def delcart(c_id):
    print(c_id)
    cart1 = Cart.query.filter_by(c_id=c_id).first()
    print(cart1)
    db.session.delete(cart1)
    db.session.commit()
    print("deleted")
    return redirect(url_for('cart'))

@app.route("/checkout",methods=['GET', 'POST'])
@login_required
def checkout():
    user = current_user.query.filter_by(id=current_user.id).first()
    cart2 = Cart.query.filter_by(c_userid=user.id).all()
    cartitems = Cart.query.filter_by(c_userid=user.id).count()
    ct = 0
    for i in cart2:
        ctotal = (i.c_p_price)
        ct = ct + ctotal

    if request.method == 'POST':
        user = current_user.query.filter_by(id=current_user.id).first()
        cart = Cart.query.filter_by(c_userid=user.id).first()
        cartitems = Cart.query.filter_by(c_userid=user.id).count()

        o_username = request.form.get('username')
        o_userid = user.id
        o_email = request.form.get('email')
        o_address = request.form.get('address')
        o_mobile = request.form.get('mobile')
        o_method = request.form.get('method')
        o_total = request.form.get('total')
        o_status = "Pending"
        o_bkash = request.form.get('bmobile')
        o_trxid = request.form.get('trxid')
        p_ownerid = cart.cownerid
        cart_id = cart.c_id
        #print(cart[1].cart_id)
        

        new_order = Order(o_username=o_username, o_userid=o_userid, o_email=o_email, o_address=o_address, o_mobile=o_mobile, o_method=o_method, o_total=o_total, o_status=o_status, o_bkash=o_bkash, o_trxid=o_trxid, p_ownerid=p_ownerid, cart_id=cart_id)
        db.session.add(new_order)
        db.session.commit()

        cart1 = Cart.query.filter_by(c_id=cart.c_id).first()
        db.session.delete(cart1)
        db.session.commit()

        return redirect(url_for('orderList',user=user, cart=cart2, cartitems=cartitems, ctotal=ct))

    return render_template('checkout.html',user=user, cart=cart2, cartitems=cartitems, ctotal=ct)
    

app.route("/order",methods=['GET', 'POST'])
@login_required
def order():
    user = current_user.query.filter_by(id=current_user.id).first()
    cart = Cart.query.filter_by(c_userid=user.id).all()
    cartitems = Cart.query.filter_by(c_userid=user.id).count()
    ct = 0
    for i in cart:
        ctotal = (i.c_p_price)
        ct = ct + ctotal

    if request.method == 'POST':
        user = current_user.query.filter_by(id=current_user.id).first()
        cart = Cart.query.filter_by(c_userid=user.id).all()
        cartitems = Cart.query.filter_by(c_userid=user.id).count()
        ct = 0
        for i in cart:
            ctotal = (i.c_p_price)
            ct = ct + ctotal
        username = user.username
        userid = user.id
        email = user.email
        address = user.address
        mobile = user.mobile
        method = request.form.get('method')
        bkash = request.form.get('bkash')
        trxid = request.form.get('trxid')
        status = "Pending"
        p_ownerid = request.form.get('p_ownerid')
        new_order = Order(o_username=username, o_userid=userid, o_email=email, o_address=address, o_mobile=mobile, o_method=method, o_total=ct, o_status=status, o_bkash=bkash, o_trxid=trxid, p_ownerid=p_ownerid)
        db.session.add(new_order)
        db.session.commit()
        return redirect(url_for('order'))
    return render_template('order.html',user=user, cart=cart, cartitems=cartitems, ctotal=ct)

@app.route("/orderList",methods=['GET', 'POST'])
@login_required
def orderList():
    user = current_user.query.filter_by(id=current_user.id).first()
    order = Order.query.filter_by(o_userid=user.id).all()
    order2 = Order.query.filter_by(p_ownerid=user.id).all()
    return render_template('orderList.html',user=user, orders=order, orders2=order2)

@app.route("/paymentReceived/<int:id>",methods=['GET', 'POST'])
@login_required
def paymentReceived(id):
    order = Order.query.filter_by(o_id=id).first()
    order.o_status = "Payment Received"
    db.session.commit()
    return redirect(url_for('orderList'))

@app.route("/productSent/<int:id>",methods=['GET', 'POST'])
@login_required
def productSent(id):
    order = Order.query.filter_by(o_id=id).first()
    order.o_status = "Product Sent to Renter"
    db.session.commit()
    return redirect(url_for('orderList'))

@app.route("/productReceived/<int:id>",methods=['GET', 'POST'])
@login_required
def productReceived(id):
    order = Order.query.filter_by(o_id=id).first()
    order.o_status = "Product Received by Renter"
    db.session.commit()
    return redirect(url_for('orderList'))

@app.route("/productReturned/<int:id>",methods=['GET', 'POST'])
@login_required
def productReturned(id):
    order = Order.query.filter_by(o_id=id).first()
    order.o_status = "Product Returned to Owner"
    db.session.commit()
    return redirect(url_for('orderList'))

@app.route("/orderComplete/<int:id>",methods=['GET', 'POST'])
@login_required
def orderComplete(id):
    order = Order.query.filter_by(o_id=id).first()
    order.o_status = "Order Complete"
    db.session.commit()
    return redirect(url_for('orderList'))



# !!! Route Structures



if __name__ == '__main__':
    app.run(debug=True)