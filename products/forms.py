from django import forms

from .models import Product


class ProductModelForm(forms.ModelForm):
    # title = forms.CharField()
    class Meta:
        model = Product
        fields = [
            'title',
            'content'
        ]

    def clean_content(self):
        data = self.cleaned_data.get('title')
        if len(data) < 4:
            raise forms.ValidationError("This is not long enough")
        return data
