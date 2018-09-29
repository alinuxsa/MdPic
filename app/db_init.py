from server import db, User

db.create_all()
u1 =User(username='demo',password='demo1')
db.session.add(u1)
db.session.commit()
