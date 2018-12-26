import hashlib

from url_shortening.api import db


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)

    def save(self):
        db.session.add(self)
        db.session.commit()


class TinyUrl:
    _mapper = {}
    DB_SIZE = 4
    TABLE_SIZE = 4

    @staticmethod
    def hash_str(str):
        return int(hashlib.md5(str.encode()).hexdigest()[:8], 16)

    @staticmethod
    def model(key):
        db_index = TinyUrl.hash_str(key) % TinyUrl.DB_SIZE
        table_index = TinyUrl.hash_str(key[:4]) % TinyUrl.TABLE_SIZE

        bind_key = 'tiny_url_%02d' % db_index
        class_name = 'TinyUrl%02d' % table_index

        print('db: {} table: {}'.format(db_index, table_index))

        model_cls = TinyUrl._mapper.get(class_name, None)
        if not model_cls:
            model_cls = type(class_name, (BaseModel,), {
                '__module__': __name__,
                '__name__': class_name,
                '__bind_key__': bind_key,
                '__tablename__': 'tb_tinyurl_%02d' % table_index,
                'key': db.Column(db.String(6), nullable=False, index=True),
                'origin_url': db.Column(db.String(1024), nullable=False),
                'expiration': db.Column(db.DateTime, nullable=True),
            })
            TinyUrl._mapper[class_name] = model_cls

        return model_cls
