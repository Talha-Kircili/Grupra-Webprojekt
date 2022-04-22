from django import forms


hilfegesuch_priorities = (
    ("0", "Hilfe auswählen"),
    ("1", "Verständnisfrage"),
    ("2", "Technikproblem"),
    ("3", "Kritisches Problem")
)

class HilfegesuchForm(forms.Form):
    widget=forms.Select(attrs={'id': 'priority_field'})
    priority_field = forms.ChoiceField(widget = widget, choices=hilfegesuch_priorities, label = "")
