from django import forms
from .models import Notes  

class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['title','text','number', 'priority']
        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control my-5'}),
            'text':forms.Textarea(attrs={'class':'form-control mb-5'}),
            'number':forms.NumberInput(attrs={'class':'form-control mb-5'}),
            'priority':forms.Select(attrs={'class':'form-control mb-5'}),
            

        }
        labels = {'title':'Write a News Title here:'}

      
    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 5:
            raise forms.ValidationError('Title must be at least 5 characters long')
        return title