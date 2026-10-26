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
            'capacity': 'От 1 до 1000 посетители.',
            'description': 'По желание. Максимум 1000 символа.',
        }
        error_messages = {
            'name': {
                'required': 'Моля, въведете име на залата.',
                'max_length': 'Името е твърде дълго.',
            },
            'city': {
                'required': 'Моля, въведете град.',
                'max_length': 'Името на града е твърде дълго.',
            },
            'capacity': {
                'required': 'Моля, въведете капацитет.',
                'invalid': 'Капацитетът трябва да е цяло число.',
                'min_value': 'Капацитетът трябва да е поне 1.',
                'max_value': 'Капацитетът не може да е над 1000.',
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
                    'min': '1',
                    'max': '1000',
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Кратко описание на залата...',
                    'maxlength': '1000',
                }
            ),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if len(name) < 2:
            raise forms.ValidationError('Името трябва да е поне 2 символа.')

        queryset = Venue.objects.filter(name__iexact=name)
        if self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise forms.ValidationError('Зала с това име вече съществува.')

        return name

    def clean_city(self):
        city = self.cleaned_data.get('city', '').strip()
        if len(city) < 2:
            raise forms.ValidationError('Градът трябва да е поне 2 символа.')
        return city

    def clean_capacity(self):
        capacity = self.cleaned_data.get('capacity')
        if capacity is None:
            return capacity
        if capacity < 1:
            raise forms.ValidationError('Капацитетът трябва да е поне 1.')
        if capacity > 1000:
            raise forms.ValidationError('Капацитетът не може да е над 1000.')
        return capacity

    def clean_description(self):
        description = self.cleaned_data.get('description', '').strip()
        if len(description) > 1000:
            raise forms.ValidationError('Описанието не може да е над 1000 символа.')
        return description

