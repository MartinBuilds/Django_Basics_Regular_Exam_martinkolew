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
                'required': 'Моля, въведете име на изпълнителя.',
                'min_length': 'Името трябва да е поне 2 символа.',
                'max_length': 'Името е твърде дълго.',
            },
            'country': {
                'required': 'Моля, въведете държава.',
                'max_length': 'Името на държавата е твърде дълго.',
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bio'].required = False

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if len(name) < 2:
            raise forms.ValidationError('Името трябва да е поне 2 символа.')

        queryset = Performer.objects.filter(name__iexact=name)
        if self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise forms.ValidationError('Името трябва да е уникално.')

        return name

    def clean_country(self):
        country = self.cleaned_data.get('country', '').strip()
        if not country:
            raise forms.ValidationError('Моля, въведете държава.')
        return country

    def clean_bio(self):
        return self.cleaned_data.get('bio', '').strip()
