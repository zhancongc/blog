from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    photo = db.Column(db.Unicode(64))
    nickname = db.Column(db.Unicode(64), index = True)
    phone = db.Column(db.String(11),index = True)
    email = db.Column(db.String(120), index = True, unique = True)
    business = db.Column(db.Unicode(64))
    position = db.Column(db.Unicode(64))
    remark = db.Column(db.UnicodeText)
    favorite = db.Column(db.Integer)
    interview = db.Column(db.Integer)

    def __repr__(self):
        return '<User %r>' % (self.nickname)