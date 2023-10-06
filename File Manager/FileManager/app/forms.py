from django import forms  
from .models import File

class fileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['title', 'description', 'file']

    def __init__(self, *args, **kwargs):
        super(fileForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})



# class FileSearchForm(forms.Form):
#     search_query = forms.CharField(max_length=100, required=False, label='Search Files')
