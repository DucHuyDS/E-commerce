from .models import ReviewRating
from django import  forms
from .models import Product

class ReviewForm(forms.ModelForm):
    class Meta:
        model=ReviewRating
        fields=['title','description','rating']
