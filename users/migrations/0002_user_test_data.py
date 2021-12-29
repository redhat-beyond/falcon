from django.db import migrations, transaction


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial'),
    ]

    def generate_data(apps, schema_editor):
        from users.models import User, Team, Role

        with transaction.atomic():
            team_1 = Team.objects.create(name="Team HR", description="Human Resources")
            team_2 = Team.objects.create(name="Team R&D", description="Research and development")
            Team.objects.create(name="Team QA", description="Quality Assurance")

            User.create_user(
                username="emp1",
                email="user1@redhat.com",
                password="password",
                first_name="Eyal",
                last_name="Golan",
                role=Role.EMPLOYEE,
                team=team_1)

            User.create_user(
                username="emp11",
                email="user1@redhat.com",
                password="password",
                first_name="Lior",
                last_name="Nakris",
                role=Role.EMPLOYEE,
                team=team_1)

            User.create_user(
                username="emp2",
                email="user1@redhat.com",
                password="password",
                first_name="Zehava",
                last_name="Ben",
                role=Role.EMPLOYEE,
                team=team_2)

            User.create_user(
                username="man1",
                email="user1@redhat.com",
                password="password",
                first_name="Sarit",
                last_name="Hadad",
                role=Role.MANAGER,
                team=team_1)

            User.create_user(
                username="man2",
                email="user1@redhat.com",
                password="password",
                first_name="Eden",
                last_name="Hason",
                role=Role.MANAGER,
                team=team_2)

    operations = [
        migrations.RunPython(generate_data),
    ]
