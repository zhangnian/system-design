from url_shortening.api import app, db


def create_db():
    db.create_all()


def main():
    app.run(debug=True)


if __name__ == '__main__':
    #create_db()
    main()
