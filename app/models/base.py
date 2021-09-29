from contextlib import contextmanager

from flask_sqlalchemy import BaseQuery
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy
from sqlalchemy import inspect, orm, desc


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e


db = SQLAlchemy(query_class=BaseQuery)


class Base(db.Model):
    __abstract__ = True
    __table_args__ = {"useexisting": True}

    def __getitem__(self, item):
        return getattr(self, item)

    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

    def keys(self):
        return self.fields

    def hide(self, *keys):
        for key in keys:
            self.fields.remove(key)
        return self

    def append(self, *keys):
        for key in keys:
            self.fields.append(key)
        return self

    @classmethod
    def get_by_id(cls, id_):
        return cls.query.get(id_)

    @classmethod
    def modify(cls, id_, **kwargs):
        base = cls.get_by_id(id_)
        with db.auto_commit():
            for key, value in kwargs.items():
                if value is not None and value != '':
                    if hasattr(cls, key):
                        setattr(base, key, value)

    @classmethod
    def search(cls, **kwargs):
        res = cls.query
        for key, value in kwargs.items():
            if value is not None and value != '':
                try:
                    value = int(value)
                except (ValueError, TypeError):
                    pass
                if hasattr(cls, key):
                    if isinstance(value, int):
                        res = res.filter(getattr(cls, key) == value)
                    elif isinstance(value, list):
                        res = res.filter(getattr(cls, key).in_(value))
                    else:
                        res = res.filter(getattr(cls, key).like(value))

        data = {
            'count': res.count()
        }
        try:
            res = res.order_by(desc(cls.id))
        except AttributeError:
            pass
        page = int(kwargs.get('page', 1))
        page_size = int(kwargs.get('page_size', 20))
        res = res.offset((page - 1) * page_size).limit(page_size)
        res = res.all()
        data['data'] = res
        return data


class MixinJSONSerializer:
    @orm.reconstructor
    def init_on_load(self):
        self._fields = []
        # self._include = []
        self._exclude = []

        self._set_fields()
        self.__prune_fields()

    def _set_fields(self):
        pass

    def __prune_fields(self):
        columns = inspect(self.__class__).columns
        if not self._fields:
            all_columns = set(columns.keys())
            self._fields = list(all_columns - set(self._exclude))

    def hide(self, *args):
        for key in args:
            self._fields.remove(key)
        return self

    def keys(self):
        return self._fields

    def __getitem__(self, key):
        return getattr(self, key)
