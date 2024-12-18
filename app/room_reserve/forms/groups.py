from django import forms
from room_reserve.models import Group


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ["name", "description", "group_type"]
