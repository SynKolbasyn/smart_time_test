# Generated by Django 5.2a1 on 2025-02-12 12:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Room",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("rum_number", models.IntegerField()),
            ],
            options={
                "db_table": "rooms",
            },
        ),
        migrations.CreateModel(
            name="Exam",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("subject_name", models.TextField()),
                (
                    "room_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="api.room",
                    ),
                ),
            ],
            options={
                "db_table": "exams",
            },
        ),
    ]
