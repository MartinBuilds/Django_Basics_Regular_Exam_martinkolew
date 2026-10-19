from django import forms

from .models import Performer


class PerformerForm(forms.ModelForm):
    class Meta:
        model = Performer
        fields = ('name', 'country', 'bio')
        labels = {
            'name': 'Име',
            'country': 'Държава',
            'bio': 'Биография',
        }
        help_texts = {
            'bio': 'По желание.',
        }
        error_messages = {
            'name': {
                'required': 'Моля, въведи име на изпълнителя.',
            },
            'country': {
                'required': 'Моля, въведи държава.',
            },
        }
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Напр. The Foo Fighters',
                }
            ),
            'country': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Напр. България',
                }
            ),
            'bio': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Кратка биография...',
                }
            ),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            queryset = Performer.objects.filter(name__iexact=name)
            if self.instance.pk:
                queryset = queryset.exclude(pk=self.instance.pk)
            if queryset.exists():
                raise forms.ValidationError('Изпълнител с това име вече съществува.')
        return name