from django.db import migrations, transaction


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial'),
    ]

    def generate_data(apps, schema_editor):
        from users.models import User, Team, Role

        with transaction.atomic():
            team_1 = Team.objects.create(name="HR Team", description="Human Resources")
            team_2 = Team.objects.create(name="R&D Team", description="Research and development")
            Team.objects.create(name="QA Team", description="Quality Assurance")

            users_data = [
                ("employee111", "user1@redhat.com", "password", "Eyal", "Golan", Role.EMPLOYEE, team_1),
                ("employee1111", "user11@redhat.com", "password", "Lior", "Nakris", Role.EMPLOYEE, team_1),
                ("employee22", "user2@redhat.com", "password", "Zehava", "Ben", Role.EMPLOYEE, team_2),
                ("manager11", "user13@redhat.com", "password", "Sarit", "Hadad", Role.MANAGER, team_1),
                ("manager22", "user14@redhat.com", "password", "Eden", "Hason", Role.MANAGER, team_2),
            ]

            for username, email, password, first_name, last_name, role, team in users_data:
                User.create_user(username=username, email=email, password=password, first_name=first_name,
                                 last_name=last_name, role=role, team=team)

    operations = [
        migrations.RunPython(generate_data),
    ]
