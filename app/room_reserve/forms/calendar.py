from django import forms
from room_reserve.models import Meeting, Event


class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = [
            "name_pl",
            "name_en",
            "start_time",
            "end_time",
            "meeting_type",
            "room",
            "description",
            "lecturers",
            "capacity",
            "color",
            "is_updated",
            "event",
        ]
        widgets = {
            "start_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "description": forms.Textarea(attrs={"placeholder": "Opis spotkania", "rows": 3}),
            "lecturers": forms.SelectMultiple(attrs={"size": "5"}),
            "color": forms.TextInput(attrs={"type": "color"}),
            "event": forms.Select(attrs={"placeholder": "Wybierz wydarzenie"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customization of form field labels or placeholders can go here
        self.fields["name_pl"].widget.attrs.update({"placeholder": "Wprowadź nazwę w języku polskim"})
        self.fields["name_en"].widget.attrs.update({"placeholder": "Wprowadź nazwę w języku angielskim"})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["meeting_type"].choices = [("meeting", "Spotkanie"), ("classgroup", "Grupa zajęciowa")]
        self.fields["event"].queryset = Event.objects.all()
        self.fields["event"].required = False


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
