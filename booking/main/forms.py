from django import forms

class availabilityForm(forms.Form):
    check_in = forms.DateTimeField(required=True, input_formats=[ '%m/%d/%y %H:%M:%S'] )
    check_out = forms.DateTimeField(required=True, input_formats=[ '%m/%d/%y %H:%M:%S'] )