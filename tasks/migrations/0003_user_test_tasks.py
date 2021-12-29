from django.db import migrations, transaction


class Migration(migrations.Migration):
    dependencies = [
        ('tasks', '0001_initial'),
        ('tasks', '0002_initial'),
        ('users', '0001_initial'),
        ('users', '0002_user_test_data'),
    ]

    def generate_data(apps, schema_editor):
        from tasks.models import Task, Priority, Status, Comment
        from users.models import User

        with transaction.atomic():
            employee_1 = User.objects.get(user__username="emp1")
            employee_11 = User.objects.get(user__username="emp11")
            employee_2 = User.objects.get(user__username="emp2")
            manager_1 = User.objects.get(user__username="man1")
            manager_2 = User.objects.get(user__username="man2")

            task_11 = Task.objects.create(title="task 11",
                                          assignee=employee_1,
                                          created_by=manager_1,
                                          priority=Priority.HIGH,
                                          status=Status.IN_PROGRESS,
                                          description="build me a house")

            task_12 = Task.objects.create(title="task 12",
                                          assignee=employee_11,
                                          created_by=manager_1,
                                          priority=Priority.HIGH,
                                          status=Status.IN_PROGRESS,
                                          description="sing me a song")

            task_13 = Task.objects.create(title="task 13",
                                          assignee=employee_1,
                                          created_by=manager_1,
                                          priority=Priority.HIGH,
                                          status=Status.IN_PROGRESS,
                                          description="task 13 description")

            task_14 = Task.objects.create(title="task 14",
                                          assignee=employee_11,
                                          created_by=manager_1,
                                          priority=Priority.HIGH,
                                          status=Status.IN_PROGRESS,
                                          description="task 14 description")

            task_21 = Task.objects.create(title="task 21",
                                          assignee=employee_2,
                                          created_by=manager_2,
                                          priority=Priority.HIGH,
                                          status=Status.IN_PROGRESS,
                                          description="task 21 description")

            task_22 = Task.objects.create(title="task 22",
                                          assignee=employee_2,
                                          created_by=manager_2,
                                          priority=Priority.HIGH,
                                          status=Status.IN_PROGRESS,
                                          description="task 22 description")

            Comment.objects.create(appUser=employee_1,
                                   task=task_11,
                                   title="A problem",
                                   description="I dont know how")

            Comment.objects.create(appUser=employee_11,
                                   task=task_11,
                                   title="A problem2",
                                   description="I dont know how2")

            Comment.objects.create(appUser=employee_11,
                                   task=task_12,
                                   title="A problem2",
                                   description="I dont know how2")

            Comment.objects.create(appUser=employee_1,
                                   task=task_12,
                                   title="A problem2",
                                   description="I dont know how2")

            Comment.objects.create(appUser=employee_11,
                                   task=task_13,
                                   title="A problem2",
                                   description="I dont know how2")

            Comment.objects.create(appUser=employee_1,
                                   task=task_13,
                                   title="A problem",
                                   description="I dont know how")

            Comment.objects.create(appUser=employee_1,
                                   task=task_14,
                                   title="A problem",
                                   description="I dont know how")

            Comment.objects.create(appUser=employee_11,
                                   task=task_14,
                                   title="A problem2",
                                   description="I dont know how2")

            Comment.objects.create(appUser=employee_2,
                                   task=task_21,
                                   title="A problem",
                                   description="I dont know how")

            Comment.objects.create(appUser=manager_2,
                                   task=task_21,
                                   title="A problem2",
                                   description="I dont know how2")

            Comment.objects.create(appUser=employee_2,
                                   task=task_22,
                                   title="A problem",
                                   description="I dont know how")

            Comment.objects.create(appUser=manager_2,
                                   task=task_22,
                                   title="A problem2",
                                   description="I dont know how2")

    operations = [
        migrations.RunPython(generate_data),
    ]
