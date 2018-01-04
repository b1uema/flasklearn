from hellodog import db
def createdb():
    db.create_all()


if __name__ == "__main__":
    createdb()