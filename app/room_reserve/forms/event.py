from django import forms
from django.forms import inlineformset_factory
from room_reserve.models import Event, Meeting


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'organizer', 'event_type', 'start_date', 'end_date']


# Inline formset for meetings associated with an event
MeetingFormSet = inlineformset_factory(
    Event, Meeting, 
    fields=['meeting_type', 'start_time', 'end_time', 'name_pl', 'name_en', 'room', 'description', 'lecturers', 'capacity', 'color'],
    extra=1,  # Number of extra empty forms to show
    can_delete=True  # Allow deleting meetings in the formset
)