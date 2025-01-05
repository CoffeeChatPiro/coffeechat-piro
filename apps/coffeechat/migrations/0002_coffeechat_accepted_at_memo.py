# Generated by Django 4.2.17 on 2025-01-05 10:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("coffeechat", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="coffeechat",
            name="accepted_at",
            field=models.DateTimeField(null=True),
        ),
        migrations.CreateModel(
            name="Memo",
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
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("content", models.CharField(blank=True, max_length=5000)),
                (
                    "coffeeChatRequest",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="memo",
                        to="coffeechat.coffeechat",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="memos",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
