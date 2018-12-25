from url_shortening.api import db


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)

    def save(self):
        db.session.add(self)
        db.session.commit()


class TinyUrl(BaseModel):
    __tablename__ = 'tb_tinyurl'

    key = db.Column(db.String(6), nullable=False, index=True)
    origin_url = db.Column(db.String(1024), nullable=False)
    expiration = db.Column(db.DateTime, nullable=True)
