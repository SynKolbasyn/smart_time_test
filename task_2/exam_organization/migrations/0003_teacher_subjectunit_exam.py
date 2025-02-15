# Generated by Django 5.2a1 on 2025-02-15 09:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "exam_organization",
            "0002_alter_campus_table_alter_subject_table_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="Teacher",
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
                ("forename", models.TextField()),
                ("surname", models.TextField()),
                ("patronymic", models.TextField()),
                ("passport_number", models.IntegerField(unique=True)),
                (
                    "type",
                    models.TextField(
                        choices=[
                            ("lecturer", "Lecturer"),
                            ("seminarian", "Seminarian"),
                        ]
                    ),
                ),
            ],
            options={
                "db_table": "teachers",
            },
        ),
        migrations.CreateModel(
            name="SubjectUnit",
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
                (
                    "group_type",
                    models.CharField(
                        choices=[
                            ("П", "Flow"),
                            ("Г", "Group"),
                            ("С", "Sub Group"),
                        ],
                        max_length=1,
                    ),
                ),
                ("group_number", models.IntegerField(unique=True)),
                (
                    "campus",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="exam_organization.campus",
                    ),
                ),
                (
                    "subject",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="exam_organization.subject",
                    ),
                ),
            ],
            options={
                "db_table": "subject_units",
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
                (
                    "subject_unit",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="exam_organization.subjectunit",
                    ),
                ),
            ],
            options={
                "db_table": "exams",
            },
        ),
    ]
