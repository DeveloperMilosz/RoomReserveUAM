from django import forms
from room_reserve.views.calendar import Meeting
from room_reserve.views.calendar import Event

class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = [
            'name_pl', 'name_en', 'start_time', 'end_time', 'meeting_type', 'room', 
            'description', 'lecturers', 'capacity', 'color', 'is_updated'
        ]
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'placeholder': 'Opis wydarzenia', 'rows': 3}),
            'lecturers': forms.SelectMultiple(attrs={'size': '5'}),
            'color': forms.TextInput(attrs={'type': 'color'}),
        }

    def __init__(self, *args, **kwargs):
        super(MeetingForm, self).__init__(*args, **kwargs)
        self.fields['meeting_type'].widget = forms.Select(
            choices=[("meeting", "Spotkanie"), ("classgroup", "Grupa zajęciowa")]
        )

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'event_type', 'start_date', 'end_date', 'organizer']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'placeholder': 'Opis wydarzenia', 'rows': 3}),
        }
        
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['event_type'].widget = forms.Select(
            choices=[("lesson_schedule", "Plan zajęć"), ("event", "Wydarzenie")]
        )