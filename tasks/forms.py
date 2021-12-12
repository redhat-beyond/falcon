from django import forms
from .models import Task, Priority, Status, User


class TaskForm(forms.ModelForm):
    def __init__(self, user_id, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        logged_user = User.objects.filter(user_id=user_id)
        self.fields['created_by'].queryset = logged_user
        self.initial['created_by'] = logged_user.first()

    class Meta:
        model = Task
        fields = ('title', 'assignee', 'created_by', 'priority', 'status', 'description')
        priority_choices = [('LOW', Priority.LOW), ('MEDIUM', Priority.MEDIUM), ('HIGH', Priority.HIGH),
                            ('CRITICAL', Priority.CRITICAL)]
        status_choices = [('BACKLOG', Status.BACKLOG), ('IN_PROGRESS', Status.IN_PROGRESS), ('DONE', Status.DONE)]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'assignee': forms.Select(attrs={'class': 'form-control'}),
            'created_by': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(choices=priority_choices, attrs={'class': 'form-control'}),
            'status': forms.Select(choices=status_choices, attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ('status',)
