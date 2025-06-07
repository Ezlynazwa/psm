# recommendation/forms.py

from django import forms
from .models import SkinAssessment
from store.models import Product  # for pulling choices if needed


class SkinAssessmentForm(forms.ModelForm):
    concerns = forms.MultipleChoiceField(
        choices=SkinAssessment.CONCERN_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    def clean_concerns(self):
        concerns = self.cleaned_data.get('concerns', [])
        # Validate each concern is in available choices
        valid_concerns = [choice[0] for choice in SkinAssessment.CONCERN_CHOICES]
        for concern in concerns:
            if concern not in valid_concerns:
                raise forms.ValidationError(f"Invalid concern selected: {concern}")
        return concerns

    class Meta:
        model = SkinAssessment
        fields = [
            'skin_type', 'undertone', 'concerns', 'hydration_level', 'oiliness_level',
            'sensitivity_level', 'acne_proneness', 'aging_concerns',
            'finish_preference', 'texture_preference',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pre-populate the checkbox if editing
        if self.instance and self.instance.concerns:
            self.initial['concerns'] = self.instance.concerns.split(',')

    def save(self, commit=True):
        inst = super().save(commit=False)
        inst.concerns = ",".join(self.cleaned_data.get('concerns', []))
        if commit:
            inst.save()
        return inst
