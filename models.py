import orm_sqlite


class Spreadsheet(orm_sqlite.Model):
    id = orm_sqlite.IntegerField(primary_key=True)
    name = orm_sqlite.StringField()
    amount = orm_sqlite.FloatField()
    date = orm_sqlite.StringField()