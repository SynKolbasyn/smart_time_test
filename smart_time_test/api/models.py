from django.db.models import EmailField, Model, TextField


class User(Model):
    email = EmailField()
    password = TextField()

    class Meta:
        db_table = "users"
