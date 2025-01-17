from django import forms
from room_reserve.models import Meeting, Event, Room, Lecturers, Note, Group, User

class MeetingForm(forms.ModelForm):
    is_recurring = forms.BooleanField(required=False, initial=False)
    frequency_select = forms.ChoiceField(
        choices=[
            ('daily', 'Codziennie'),
            ('weekly', 'Co tydzień'),
            ('biweekly', 'Co drugi tydzień'),
            ('monthly', 'Co miesiąc'),
            ('custom_days', 'Wybierz dni'),
        ],
        required=False,
    )
    days_of_week = forms.MultipleChoiceField(
        choices=[
            ('0', 'Poniedziałek'),
            ('1', 'Wtorek'),
            ('2', 'Środa'),
            ('3', 'Czwartek'),
            ('4', 'Piątek'),
            ('5', 'Sobota'),
            ('6', 'Niedziela'),
        ],
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    cycle_end_date = forms.DateField(required=False)
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        label="Groups",
        help_text="Associate this meeting with multiple groups.",
        widget=forms.SelectMultiple(attrs={'size': '5'})
    )

    class Meta:
        model = Meeting
        fields = [
            'name_pl', 'name_en', 'start_time', 'end_time', 'meeting_type', 'room',
            'description', 'lecturers', 'capacity', 'color', 'is_updated', 'event', 'groups'
        ]
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'placeholder': 'Opis spotkania', 'rows': 3}),
            'lecturers': forms.SelectMultiple(attrs={'size': '5'}),
            'color': forms.TextInput(attrs={'type': 'color'}),
            'event': forms.Select(attrs={'placeholder': 'Wybierz wydarzenie'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['meeting_type'].choices = [
            ("meeting", "Spotkanie"),
            ("classgroup", "Grupa zajęciowa"),
        ]
        self.fields['event'].queryset = Event.objects.all()
        self.fields['room'].queryset = Room.objects.all()
        self.fields['lecturers'].queryset = User.objects.filter(user_type__in=["Lecturer", "Organizer"])
        self.fields['groups'].queryset = Group.objects.all()  # Populate available groups


class EditMeetingForm(forms.ModelForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'size': 5}),
        label="Associated Groups",
        help_text="Select all groups associated with this meeting."
    )

    class Meta:
        model = Meeting
        fields = [
            'name_pl', 'name_en', 'start_time', 'end_time', 'meeting_type',
            'description', 'room', 'lecturers', 'event', 'color', 'capacity', 'groups'
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
            'lecturers': forms.SelectMultiple(attrs={'size': '5'}),
            'event': forms.Select(attrs={'id': 'id_event'}),
            'color': forms.TextInput(attrs={'type': 'color', 'id': 'id_color'}),
            'capacity': forms.NumberInput(attrs={'id': 'capacity', 'maxlength': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['room'].queryset = Room.objects.all()
        self.fields['lecturers'].queryset = User.objects.filter(user_type__in=["Lecturer", "Organizer"])
        self.fields['event'].queryset = Event.objects.all()
        self.fields['groups'].queryset = Group.objects.all()

class EventForm(forms.ModelForm):
    organizers = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(user_type__in=["Lecturer", "Organizer"]),
        widget=forms.SelectMultiple(attrs={"class": "form-control"}),  # Multi-select dropdown
        required=False,
    )
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),  # Dropdown for single group selection
    )

    class Meta:
        model = Event
        fields = [
            "name",
            "event_type",
            "start_date",
            "end_date",
            "description",
            "organizers",  # Updated to use the new field
            "group",
            "color",
            "logo",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Event Name"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Event Description"}),
            "start_date": forms.DateTimeInput(attrs={"type": "datetime-local", "class": "form-control"}),
            "end_date": forms.DateTimeInput(attrs={"type": "datetime-local", "class": "form-control"}),
            "color": forms.TextInput(attrs={"type": "color", "class": "form-control"}),
            "logo": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }
        
class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["title", "description", "color", "status", "deadline"]
        widgets = {
            "deadline": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "color": forms.TextInput(attrs={"type": "color"}),
        }