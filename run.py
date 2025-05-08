from IDEA import app, db

if __name__ == '__main__':
    with app.app_context():  # Asegúrate de estar en el contexto de la app
        db.create_all()  # Crear las tablas si no existen
    app.run(debug=True)