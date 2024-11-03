from django import forms
from room_reserve.views.calendar import Meeting

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