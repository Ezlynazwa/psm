from django import forms
from .models import SkinProfile
from store.models import Product

class SkinAssessmentForm(forms.ModelForm):
    concerns = forms.MultipleChoiceField(
        choices=Product.SKIN_CONDITIONS,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    
    class Meta:
        model = SkinProfile
        fields = [
            'skin_type', 
            'concerns',
            'undertone',
            'sensitivity',
            'texture_preference',
            'finish_preference'
        ]