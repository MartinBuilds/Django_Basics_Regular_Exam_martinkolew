from django import forms

from .models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = (
            'title',
            'description',
            'start_datetime',
            'end_datetime',
            'ticket_price',
            'venue',
            'performers',
        )
        labels = {
            'title': 'Заглавие',
            'description': 'Описание',
            'start_datetime': 'Начало',
            'end_datetime': 'Край',
            'ticket_price': 'Цена на билет',
            'venue': 'Зала',
            'performers': 'Изпълнители',
        }
        help_texts = {
            'ticket_price': 'В лева. За безплатно събитие въведете 0.',
            'performers': 'Изберете поне един изпълнител.',
            'venue': 'Ако списъкът е празен, първо добавете зала.',
        }
        error_messages = {
            'title': {
                'required': 'Моля, въведете заглавие.',
            },
            'description': {
                'required': 'Моля, въведете описание.',
            },
            'start_datetime': {
                'required': 'Моля, въведете начална дата и час.',
                'invalid': 'Невалидна дата и час.',
            },
            'end_datetime': {
                'required': 'Моля, въведете крайна дата и час.',
                'invalid': 'Невалидна дата и час.',
            },
            'ticket_price': {
                'required': 'Моля, въведете цена.',
                'invalid': 'Цената трябва да е число.',
            },
            'venue': {
                'required': 'Моля, изберете зала.',
            },
            'performers': {
                'required': 'Моля, изберете поне един изпълнител.',
            },
        }
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Напр. Летен концерт',
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Кратко описание на събитието...',
                }
            ),
            'start_datetime': forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M',
                attrs={
                    'class': 'form-control',
                    'type': 'datetime-local',
                }
            ),
            'end_datetime': forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M',
                attrs={
                    'class': 'form-control',
                    'type': 'datetime-local',
                }
            ),
            'ticket_price': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Напр. 25.00',
                    'step': '0.01',
                }
            ),
            'venue': forms.Select(
                attrs={
                    'class': 'form-select',
                }
            ),
            'performers': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_datetime'].input_formats = ['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M:%S']
        self.fields['end_datetime'].input_formats = ['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M:%S']

    def clean_ticket_price(self):
        ticket_price = self.cleaned_data.get('ticket_price')
        if ticket_price is not None and ticket_price < 0:
            raise forms.ValidationError('Цената не може да е отрицателна.')
        return ticket_price

    def clean(self):
        cleaned_data = super().clean()
        start_datetime = cleaned_data.get('start_datetime')
        end_datetime = cleaned_data.get('end_datetime')
        performers = cleaned_data.get('performers')

        if start_datetime and end_datetime and end_datetime < start_datetime:
            raise forms.ValidationError(
                'Крайната дата трябва да е след или равна на началната.'
            )

        if performers is not None and not performers.exists():
            self.add_error('performers', 'Моля, изберете поне един изпълнител.')

        return cleaned_data


class EventFilterForm(forms.Form):
    q = forms.CharField(
        required=False,
        label='Търсене',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Търси по заглавие...',
            }
        ),
    )
    sort = forms.ChoiceField(
        required=False,
        label='Сортиране',
        choices=(
            ('', 'По подразбиране'),
            ('date_asc', 'Най-ранни първо'),
            ('date_desc', 'Най-късни първо'),
            ('title', 'Заглавие А-Я'),
            ('title_desc', 'Заглавие Я-А'),
        ),
        widget=forms.Select(
            attrs={
                'class': 'form-select',
            }
        ),
    )