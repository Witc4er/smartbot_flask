from flask import Flask, render_template, request, redirect
from db.models import Note, Tag, db_session

app = Flask(__name__)
app.debug = True


@app.route("/", strict_slashes=False)
def index():
    return render_template("index.html")

@app.route('/notes/', strict_slashes=False)
def notes():
    _notes = db_session.query(Note).all()
    return render_template('notes.html', notes=_notes)


@app.route('/note_detail/<id>', strict_slashes=False)
def detail(id):
    note = db_session.query(Note).filter(Note.id == id).first()
    return render_template('note_detail.html', note=note)


@app.route('/note_create/', methods=['GET', 'POST'], strict_slashes=False)
def note_create():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        tags = request.form.get('tags')
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


@app.route('/tag/', methods=['GET', 'POST'], strict_slashes=False)
def add_tag():
    if request.method == 'POST':
        name = request.form.get('name')
        tag = Tag(name=name)
        db_session.add(tag)
        db_session.commit()
        return redirect('/notes/')
    return render_template('tag.html')

if __name__ == '__main__':
    app.run()