from django import forms

from .models import Venue


class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = ('name', 'city', 'capacity', 'description')
        labels = {
            'name': 'Име',
            'city': 'Град',
            'capacity': 'Капацитет',
            'description': 'Описание',
        }
        help_texts = {
            'capacity': 'Максимален брой посетители.',
            'description': 'По желание.',
        }
        error_messages = {
            'name': {
                'required': 'Моля, въведете име на мястото.',
            },
            'city': {
                'required': 'Моля, въведете град.',
            },
            'capacity': {
                'required': 'Моля, въведете капацитет.',
                'invalid': 'Капацитетът трябва да е число.',
            },
        }
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Напр. Зала Универсиада',
                }
            ),
            'city': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Напр. София',
                }
            ),
            'capacity': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Напр. 500',
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Кратко описание на мястото...',
                }
            ),
        }

    def clean_capacity(self):
        capacity = self.cleaned_data.get('capacity')
        if capacity is not None and capacity < 1:
            raise forms.ValidationError('Капацитетът трябва да е поне 1.')
        return capacity