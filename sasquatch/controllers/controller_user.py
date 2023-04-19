from sasquatch import app
from flask import render_template, redirect, request, session
from sasquatch.models.model_sighting import Sighting, User, bcrypt, flash


@app.route('/')
def dash():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    # validate the form here ...
    # create the hash
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    # put the pw_hash into the data dictionary
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        "email": request.form['email'],
        "password" : pw_hash
    }
    print(data)
    if not User.valid_register(request.form):
        return redirect('/')
    # Call the create @classmethod on User
    user_id = User.create(data)
    # store user id into session
    session['user_id'] = user_id
    return redirect("/")

@app.route('/login', methods=['post'])
def login():
    # see if the username provided exists in the database
    data = { "email" : request.form["email"] }
    user_in_db = User.login(data)
    # user is not registered in the db
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid Email/Password")
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id
    session['first_name'] = user_in_db.first_name
    # never render on a post!!!
    return redirect('/dashboard')

@app.route('/dashboard')
def sightings():
    user = User.user({'id': session['user_id']})
    sightings = Sighting.all_sightings()
    return render_template('sightings.html', user = user, sights = sightings)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
