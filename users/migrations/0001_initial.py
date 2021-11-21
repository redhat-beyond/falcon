from django.db import migrations, models
import enumchoicefield.fields
import django.db.models.deletion
import users.models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user',
                 models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False,
                                      to='auth.user')),
                ('role', enumchoicefield.fields.EnumChoiceField(default=users.models.Role.EMPLOYEE,
                                                                enum_class=users.models.Role, max_length=1)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='users',
                                           to='users.team')),
            ],
        ),
    ]
