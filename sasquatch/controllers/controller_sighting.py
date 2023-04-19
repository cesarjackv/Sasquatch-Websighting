from sasquatch import app
from flask import render_template, redirect, request, session
from sasquatch.models.model_sighting import Sighting, User, bcrypt, flash

@app.route('/sightings/<int:id>/edit')
def edit(id):
    user_data = {
        'id': session['user_id']
    }
    data = {
        'id' : id
    }
    user = User.user(user_data)
    info = Sighting.one_sighting(data)
    return render_template('edit.html', info = info, user = user)

@app.route('/new')
def new():
    user = User.user({'id': session['user_id']})
    return render_template('new.html', user = user)

@app.route('/sightings/<int:id>/show')
def show(id):
    user_data = {
        'id': session['user_id']
    }
    data = {
        'id' : id
    }
    user = User.user(user_data)
    info = Sighting.one_sighting(data)
    return render_template('show.html', info = info, user = user)

@app.route('/delete/<int:id>')
def delete(id):
    data = {
        'id': id
    }
    Sighting.delete_sighting(data)
    return redirect('/dashboard')

@app.route('/create', methods = ['post'])
def create():
    print(request.form)
    if not Sighting.valid_sighting(request.form):
        return redirect('/new')
    Sighting.new_sighting(request.form)
    return redirect('/dashboard')

@app.route('/sightings/<int:id>/update', methods = ['post'])
def edit_info(id):
    
    if not Sighting.valid_sighting(request.form):
        return redirect(f"/sightings/{id}/edit")
    Sighting.edit_sighting(request.form)
    return redirect('/dashboard')