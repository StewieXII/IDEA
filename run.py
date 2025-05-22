from IDEA import app, db
from flask import render_template

@app.route('/')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
