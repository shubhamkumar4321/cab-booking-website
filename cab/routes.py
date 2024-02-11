from cab import app
from flask import render_template, redirect, Flask,url_for, flash, request,session
from cab.models import Registration_Info, User
# from cab.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from cab.forms import RegisterForm, LoginForm,Booking_Form,VerifyForm,CancellationForm
from cab import db
from flask_login import login_user, logout_user, login_required, current_user
from cab.distance_calculation import find_the_distance


@app.route('/')
@app.route('/home')
def home_page():
    # if current_user.is_authenticated:
    #     if(current_user.username=="admin"):
    #         items = Registration_Info.query.all()

    #         return render_template('admin.html',items=items)


    
    # else:
        return render_template('home.html')

@app.route('/admin_page')
@login_required
def admin_page():
    return render_template('admin.html')



@app.route('/booking_page', methods=['GET', 'POST'])
@login_required
def booking_page():
    
        form=Booking_Form()
        cancel_form=CancellationForm()
        if request.method == "POST":
            sold_item = request.form.get('sold_item')
            s_item_object = Registration_Info.query.filter_by(id=sold_item).first()
            if s_item_object:
                db.session.delete(s_item_object)
                db.session.commit()
                flash("Your Ride is cancelled Successfully",category='success')


            
            if form.validate_on_submit():
                global source
                global destination
                global distance
                global price
                source=form.location.data
                source=source.capitalize()
                destination=form.destination.data
                destination=destination.capitalize()
                distance=find_the_distance(source,destination)
                price=distance*5

                session['source']=source
                session['destination']=destination
                session['distance']=distance
                session['price']=price

                
                return redirect(url_for("verify_page"))
            
               
            return redirect(url_for('booking_page'))


        if request.method == "GET":
            items = Registration_Info.query.filter_by(username=current_user.username)
            return render_template('booking.html',form=form,owned_items=items,cancel_form=cancel_form)
            

        
@app.route('/verify', methods=['GET', 'POST'])
def verify_page():
   form=VerifyForm()
   source=session['source']
   destination=session['destination']
   price=session['price']
   distance=session['distance']
   if form.validate_on_submit():
        tour_info=Registration_Info(username= current_user.username ,source=source,destination=destination,distance=distance,price=price)
        db.session.add(tour_info)
        db.session.commit()
        flash("Your booking is successful",category='success')
        return redirect(url_for('booking_page'))


   
   return render_template('verify_page.html',source=source,form=form,destination=destination,fare=price,distance=distance)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('booking_page'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()

    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            if(form.username.data=="admin"):
                items = Registration_Info.query.all()

                return render_template('admin.html',items=items)
            else:
                return redirect(url_for('booking_page'))
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))