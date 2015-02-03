# -*- encoding: utf-8 -*-
from django import forms
from django.forms.widgets import RadioChoiceInput
from helpdesk.models import State, Comment, Ticket, Project


class CommentForm(forms.ModelForm):
    state = forms.ModelChoiceField(State.objects.all(), widget=forms.RadioSelect, initial='resolved')

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['body'].label = u'Answer body'
        self.fields['body'].widget.attrs['placeholder'] = u'Enter your answer here'

    class Meta:
        model = Comment
        fields = ('body', 'state', 'internal')


class TicketForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)
        self.fields['project'].empty_label = u'- None -'
        for fieldname in self.Meta.fields:
            self.fields[fieldname].show_hidden_initial = True

    class Meta:
        model = Ticket
        fields = ['assignee', 'priority', 'project', 'state']


class FilterForm(forms.Form):
    ASSIGNEES = (
        ('me', u'Me'),
        ('all', u'All')
    )
    assignee = forms.ChoiceField(choices=ASSIGNEES)
    state = forms.ModelChoiceField(State.objects.all(), required=False, empty_label=u'All')
    project = forms.ModelChoiceField(Project.objects.all(), required=False, empty_label=u'All')