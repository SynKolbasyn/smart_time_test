from django.db.models import EmailField, IntegerField, Model, TextField


class User(Model):
    email = EmailField()
    password = TextField()

    class Meta:
        db_table = "users"


class Room(Model):
    rum_number = IntegerField()

    class Meta:
        db_table = "rooms"
