from django import forms
from room_reserve.models import Meeting, Event, Room, Lecturers

class MeetingForm(forms.ModelForm):
    is_recurring = forms.BooleanField(required=False, initial=False)
    frequency_select = forms.ChoiceField(
        choices=[
            ('daily', 'Codziennie'),
            ('weekly', 'Co tydzień'),
            ('biweekly', 'Co drugi tydzień'),
            ('monthly', 'Co miesiąc'),
            ('custom_days', 'Wybierz dni')
        ],
        required=False
    )
    days_of_week = forms.MultipleChoiceField(
        choices=[
            ('0', 'Poniedziałek'),
            ('1', 'Wtorek'),
            ('2', 'Środa'),
            ('3', 'Czwartek'),
            ('4', 'Piątek'),
            ('5', 'Sobota'),
            ('6', 'Niedziela')
        ],
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    cycle_end_date = forms.DateField(required=False)

    class Meta:
        model = Meeting
        fields = [
                        'name_pl', 'name_en', 'start_time', 'end_time', 'meeting_type', 'room', 
            'description', 'lecturers', 'capacity', 'color', 'is_updated', 'event'
        ]
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'placeholder': 'Opis spotkania', 'rows': 3}),
            'lecturers': forms.SelectMultiple(attrs={'size': '5'}),
            'color': forms.TextInput(attrs={'type': 'color'}),
            'event': forms.Select(attrs={'placeholder': 'Wybierz wydarzenie'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['meeting_type'].choices = [
            ("meeting", "Spotkanie"), 
            ("classgroup", "Grupa zajęciowa")
        ]
        self.fields['event'].queryset = Event.objects.all()
        self.fields['event'].required = False

class EditMeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = [
            'name_pl',
            'name_en',
            'start_time',
            'end_time',
            'meeting_type',
            'description',
            'room',
            'lecturers',
            'event',
            'color',
            'capacity',
        ]
        widgets = {
            'name_pl': forms.TextInput(attrs={'id': 'id_name_pl'}),
            'name_en': forms.TextInput(attrs={'id': 'id_name_en'}),
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'id': 'id_start_time'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'id': 'id_end_time'}),
            'meeting_type': forms.Select(attrs={'id': 'id_meeting_type'}),
            'description': forms.Textarea(attrs={
                'id': 'id_description',
                'rows': 3,
                'oninput': "this.style.height = '';this.style.height = this.scrollHeight + 'px'"
            }),
            'room': forms.Select(attrs={'id': 'id_room'}),
            'lecturers': forms.SelectMultiple(attrs={'id': 'id_lecturer'}),
            'event': forms.Select(attrs={'id': 'id_event'}),
            'color': forms.TextInput(attrs={'type': 'color', 'id': 'id_color'}),
            'capacity': forms.NumberInput(attrs={'id': 'capacity', 'maxlength': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['room'].queryset = Room.objects.all()
        self.fields['lecturers'].queryset = Lecturers.objects.all()
        self.fields['event'].queryset = Event.objects.all()
        self.fields['meeting_type'].choices = Meeting.MEETING_TYPE_CHOICES

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["name", "description", "event_type", "start_date", "end_date", "organizer"]
        widgets = {
            "start_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "description": forms.Textarea(attrs={"placeholder": "Opis wydarzenia", "rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["event_type"].choices = [("lesson_schedule", "Plan zajęć"), ("event", "Wydarzenie")]

