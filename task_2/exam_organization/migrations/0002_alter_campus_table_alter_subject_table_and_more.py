# Generated by Django 5.2a1 on 2025-02-15 09:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("exam_organization", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelTable(
            name="campus",
            table="campuses",
        ),
        migrations.AlterModelTable(
            name="subject",
            table="subjects",
        ),
        migrations.DeleteModel(
            name="SubjectUnit",
        ),
    ]
