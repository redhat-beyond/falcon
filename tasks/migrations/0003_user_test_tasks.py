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
            employee_1 = User.objects.get(user__username="employee111")
            employee_11 = User.objects.get(user__username="employee1111")
            employee_2 = User.objects.get(user__username="employee22")
            manager_1 = User.objects.get(user__username="manager11")
            manager_2 = User.objects.get(user__username="manager22")

            tasks_data = [
                ('task 11', employee_1, manager_1, Priority.HIGH, Status.IN_PROGRESS, 'task 11 description'),
                ('task 12', employee_11, manager_1, Priority.HIGH, Status.IN_PROGRESS, 'task 12 description'),
                ('task 13', employee_1, manager_1, Priority.HIGH, Status.IN_PROGRESS, 'task 13 description'),
                ('task 14', employee_11, manager_1, Priority.HIGH, Status.IN_PROGRESS, 'task 14 description'),
                ('task 21', employee_2, manager_2, Priority.HIGH, Status.IN_PROGRESS, 'task 21 description'),
                ('task 22', employee_2, manager_2, Priority.HIGH, Status.IN_PROGRESS, 'task 22 description'),
            ]

            for title, assignee, created_by, priority, status, desc in tasks_data:
                Task.objects.create(title=title, assignee=assignee, created_by=created_by, priority=priority,
                                    status=status, description=desc)

            comments_data = [
                (employee_1, Task.objects.get(title='task 11'), "A problem", "I dont know how"),
                (employee_11, Task.objects.get(title='task 11'), "A problem2", "I dont know how2"),
                (employee_1, Task.objects.get(title='task 12'), "A problem", "I dont know how"),
                (employee_11, Task.objects.get(title='task 12'), "A problem2", "I dont know how2"),
                (employee_1, Task.objects.get(title='task 13'), "A problem", "I dont know how"),
                (employee_11, Task.objects.get(title='task 13'), "A problem2", "I dont know how2"),
                (employee_1, Task.objects.get(title='task 14'), "A problem", "I dont know how"),
                (employee_11, Task.objects.get(title='task 14'), "A problem2", "I dont know how2"),
                (employee_2, Task.objects.get(title='task 21'), "A problem", "I dont know how"),
                (manager_2, Task.objects.get(title='task 21'), "A problem2", "I dont know how2"),
                (employee_2, Task.objects.get(title='task 22'), "A problem", "I dont know how"),
                (manager_2, Task.objects.get(title='task 22'), "A problem2", "I dont know how2"),
            ]

            for user, task, title, desc in comments_data:
                Comment.objects.create(appUser=user, task=task, title=title, description=desc)

    operations = [
        migrations.RunPython(generate_data),
    ]
