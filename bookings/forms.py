from django import forms
from .models import Space
import datetime

class BookingForm(forms.Form):
    check_in = forms.DateField(widget=forms.TextInput(attrs={
        'class': 'form-control flatpickr-input',
        'placeholder': 'Select Check-in Date',
        'autocomplete': 'off'
    }))

    check_out = forms.DateField(widget=forms.TextInput(attrs={
        'class': 'form-control flatpickr-input',
        'placeholder': 'Select Check-out Date',
        'autocomplete': 'off'
    }))

    # Optional; only required for hall bookings
    event_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter event name'
    }))

    event_date = forms.DateField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control flatpickr-input',
        'placeholder': 'Select event date',
        'autocomplete': 'off'
    }))

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get("check_in")
        check_out = cleaned_data.get("check_out")
        event_date = cleaned_data.get("event_date")
        event_name = cleaned_data.get("event_name")

        # Validation: check-out after check-in
        if check_in and check_out and check_out <= check_in:
            raise forms.ValidationError("Check-out must be after check-in date.")

        # If this is a hall booking, event_name and event_date are required
        if self.initial.get('space_type') == 'hall':
            if not event_name:
                self.add_error('event_name', "Event name is required for hall bookings.")
            if not event_date:
                self.add_error('event_date', "Event date is required for hall bookings.")
        return cleaned_data
