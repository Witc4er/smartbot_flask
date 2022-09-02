from datetime import datetime

from flask import Flask, render_template, request, redirect
from db.models import Note, Tag, db_session, AddressBook, Email, Telephone

app = Flask(__name__)
app.debug = True


@app.route("/", strict_slashes=False)
def index():
    return render_template("index.html")

@app.route('/addressbook/', strict_slashes=False)
def addressbook():
    _addressbook = db_session.query(AddressBook).all()
    return render_template('addressbook.html', addressbook=_addressbook)

@app.route('/contact_create/', methods=['GET', 'POST'], strict_slashes=False)
def contact_create():
    if request.method == 'POST':
        name = request.form.get('name')
        birthday = datetime.strptime(request.form.get('birthday'), '%Y-%m-%d').date()
        address = request.form.get('address')
        email = request.form.get('email')
        phone = request.form.get('phone')
        print(name, birthday, address, email, phone)
        contact = AddressBook(name=name,
                              birthday=birthday,
                              address=address,
                              email=[Email(email=email)],
                              phone=[Telephone(phone=phone)])
        db_session.add(contact)
        db_session.commit()
        return redirect('/addressbook/')
    else:
        pass
    return render_template('contact_create.html')

@app.route('/contact_detail/<id>', strict_slashes=False)
def contact_detail(id):
    contact = db_session.query(AddressBook).filter(AddressBook.id == id).first()
    return render_template('contact_detail.html', contact=contact)

@app.route('/contact_delete/<id>', strict_slashes=False)
def contact_delete(id):
    db_session.query(AddressBook).filter(AddressBook.id == id).delete()
    db_session.commit()
    return redirect('/addressbook/')



@app.route('/notes/', strict_slashes=False)
def notes():
    _notes = db_session.query(Note).all()
    return render_template('notes.html', notes=_notes)


@app.route('/note_create/', methods=['GET', 'POST'], strict_slashes=False)
def note_create():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        tags = request.form.getlist('tags')
        tags_obj = []
        for tag in tags:
            tags_obj.append(db_session.query(Tag).filter(Tag.name == tag).first())
        note = Note(name=name, description=description, tags=tags_obj)
        db_session.add(note)
        db_session.commit()
        return redirect('/notes/')
    else:
        tags = db_session.query(Tag).all()
    return render_template('note_create.html', tags=tags)

@app.route('/note_detail/<id>', strict_slashes=False)
def note_detail(id):
    note = db_session.query(Note).filter(Note.id == id).first()
    return render_template('note_detail.html', note=note)



@app.route('/tag/', methods=['GET', 'POST'], strict_slashes=False)
def add_tag():
    if request.method == 'POST':
        name = request.form.get('name')
        tag = Tag(name=name)
        db_session.add(tag)
        db_session.commit()
        return redirect('/notes/')
    return render_template('tag.html')

@app.route('/done/<id>', strict_slashes=False)
def done(id):
    db_session.query(Note).filter(Note.id == id).first().done = True
    db_session.commit()

    return redirect('/notes/')

@app.route('/delete/<id>', strict_slashes=False)
def note_delete(id):
    db_session.query(Note).filter(Note.id == id).delete()
    db_session.commit()

    return redirect('/notes/')

if __name__ == '__main__':
    app.run()