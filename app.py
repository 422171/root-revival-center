"""Flask Application for Root Revival Center."""
from flask import Flask, render_template, abort, flash, request
from forms import SignUpForm, LoginForm, createPlantForm, EditPlantForm
from flask import session, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

load_dotenv() 

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'change-me')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///plants.db')
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'plants')
app.config['MAX_CONTENT_LENGTH'] = 3 * 1024 * 1024  # 3MB max file size
db = SQLAlchemy(app)

"""Model for Plants."""
class Plant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    type = db.Column(db.String)
    bio = db.Column(db.String)
    posted_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    image_filename = db.Column(db.String)  # store actual filename with extension

"""Model for Users."""
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    plants = db.relationship('Plant', backref='poster')


@app.route("/")
def homepage():
    """View function for Home Page."""
    plants = Plant.query.all()
    return render_template("home.html", plants = plants)


@app.route("/about")
def about():
    """View function for About Page."""
    return render_template("about.html")

@app.route("/create", methods=["POST", "GET"])
def create_plant():
    form = createPlantForm()
    if form.validate_on_submit():
        new_plant = Plant(name=form.name.data, type=form.type.data, bio=form.bio.data, posted_by=session['user'])
        db.session.add(new_plant)
        try:
            db.session.commit()
            image_file = form.image.data
            ext = os.path.splitext(secure_filename(image_file.filename))[1]
            filename = f"{new_plant.id}{ext}"
            image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new_plant.image_filename = filename
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return render_template("create.html", form=form, message="A Plant with this name already exists!")
        finally:
            db.session.close()
        flash("Plant created successfully!")
        return redirect(url_for('dashboard'))
    return render_template("create.html", form=form)


@app.route("/plants/<int:plant_id>", methods=["POST", "GET"])
def plant_details(plant_id):
    """View and process plant details: editing and adoption."""
    plant = Plant.query.get_or_404(plant_id)

    # Edit mode: only owner with edit flag
    if session.get('user') == plant.posted_by and request.args.get('edit') == '1':
        form = EditPlantForm(obj=plant)
        if form.validate_on_submit():
            plant.name = form.name.data
            plant.type = form.type.data
            plant.bio = form.bio.data
            try:
                db.session.commit()
                flash('Edits saved successfully.')
                return redirect(url_for('plant_details', plant_id=plant.id, edit=1))
            except Exception:
                db.session.rollback()
                return render_template('details.html', plant=plant, form=form, message='Name conflict, choose another.')
        return render_template('details.html', plant=plant, form=form)

    # Adoption request or other POSTs
    if request.method == 'POST':
        if 'user' not in session:
            flash('Please log in to request adoption.')
            return redirect(url_for('login'))
        flash('Your request to adopt is registered; we will contact you soon.')
        return redirect(url_for('plant_details', plant_id=plant_id))

    # Default
    return render_template('details.html', plant=plant, form=None)

@app.route("/delete/<int:plant_id>", methods=["POST", "GET"])
def delete_plant(plant_id):
    plant = Plant.query.get(plant_id)
    if plant is None: 
        abort(404, description="No Plant was Found with the given ID")
    if request.method == 'POST':
        db.session.delete(plant)
        try:
            db.session.commit()
            flash("Plant deleted successfully.")
        except Exception:
            db.session.rollback()
        return redirect(url_for('dashboard'))
    # GET fallback
    return render_template("details.html", plant=plant, form=None)

@app.route("/details/<int:plant_id>/change_image", methods=["POST"])
def change_image(plant_id):
    plant = Plant.query.get_or_404(plant_id)
    if 'user' not in session or session.get('user') != plant.posted_by:
        abort(403)
    file = request.files.get('image_file')
    if file:
        ext = os.path.splitext(secure_filename(file.filename))[1]
        filename = f"{plant.id}{ext}"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        plant.image_filename = filename
        db.session.commit()
        flash("Image updated successfully.")
    return redirect(url_for('plant_details', plant_id=plant.id, edit=1))

@app.route("/signup", methods=["POST", "GET"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        new_user = User(full_name = form.full_name.data, email = form.email.data, password = form.password.data)
        db.session.add(new_user)
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return render_template("signup.html", form = form, message = "This Email is already registered! Please Login instead.")
        finally:
            db.session.close()
        flash("Successfully signed up ")
        return redirect(url_for('login'))
    return render_template("signup.html", form = form)


@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data, password=form.password.data).first()
        if not user:
            return render_template('login.html', form=form, message='Wrong credentials, please try again.')
        session['user'] = user.id
        flash(f'Welcome back, {user.full_name}!')
        return redirect(url_for('homepage'))
    return render_template("login.html", form = form)

@app.route("/dashboard")
def dashboard():
    if 'user' not in session:
        flash("Please log in to view your dashboard.")
        return redirect(url_for('login'))
    
    user = User.query.get(session['user'])
    user_plants = Plant.query.filter_by(posted_by=user.id).all()
    return render_template('dashboard.html', plants=user_plants, user_full_name=user.full_name)

@app.route("/logout")
def logout():
    if 'user' in session:
        session.pop('user')
        flash("You have been logged out.")
    return redirect(url_for('homepage'))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
    
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)
