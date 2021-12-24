from django import forms
from .models import Comment, Task, Priority, Status, User, Role


class TaskForm(forms.ModelForm):
    def __init__(self, user_id, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        logged_user = User.objects.filter(user_id=user_id)
        assignee_list = User.objects.filter(team=logged_user.first().team, role=Role.EMPLOYEE)
        choices = []
        for user in assignee_list:
            choices.append((user.user.id, f'{user.user.first_name} {user.user.last_name}'))
        self.fields['assignee'].choices = choices
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
            'created_by': forms.HiddenInput,
            'priority': forms.Select(choices=priority_choices, attrs={'class': 'form-control'}),
            'status': forms.Select(choices=status_choices, attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }


class ViewTaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        self.fields['status'].label = ''

    class Meta:
        model = Task
        fields = ('status',)
        widgets = {
            'status': forms.Select(choices=TaskForm.Meta.status_choices,
                                   attrs={'class': 'form-control-sm mt-1', 'style': "vertical-align: middle"}),
         }


class CommentForm(forms.ModelForm):
    description = forms.CharField(required=True, strip=True, max_length=999,
                                  widget=forms.Textarea(attrs={
                                                 'class': 'form-control w-50',
                                                 'rows': '4',
                                                 'placeholder': 'Add new comment ...'}),
                                  error_messages={'required': 'Comment must contain text !'})

    def __init__(self, user, task, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['description'].label = ''
        self.user = user
        self.task = task

    class Meta:
        model = Comment
        fields = ('description',)
