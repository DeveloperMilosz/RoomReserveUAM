from django import forms
from django.forms import inlineformset_factory
from room_reserve.models import Event, Meeting, Group

class EventForm(forms.ModelForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=forms.SelectMultiple,
        label="Groups"
    )

    class Meta:
        model = Event
        fields = ['name', 'description', 'organizer', 'event_type', 'start_date', 'end_date', 'color', 'groups']