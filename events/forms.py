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
            'ticket_price': 'Цена на билет (€)',
            'venue': 'Зала',
            'performers': 'Изпълнители',
        }
        help_texts = {
            'title': 'Поне 3 символа.',
            'description': 'Максимум 1000 символа.',
            'ticket_price': 'От 0 до 1000 €. За безплатно събитие въведете 0.',
            'performers': 'Изберете поне един изпълнител.',
            'venue': 'Ако списъкът е празен, първо добавете зала.',
        }
        error_messages = {
            'title': {
                'required': 'Моля, въведете заглавие.',
                'min_length': 'Заглавието трябва да е поне 3 символа.',
                'max_length': 'Заглавието е твърде дълго.',
            },
            'description': {
                'required': 'Моля, въведете описание.',
                'max_length': 'Описанието не може да е над 1000 символа.',
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
                'min_value': 'Цената не може да е отрицателна.',
                'max_value': 'Цената не може да е над 1000 €.',
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
                    'maxlength': '1000',
                }
            ),

            'start_datetime': forms.DateTimeInput(
                format='%d.%m.%Y %H:%M',
                attrs={
                    'class': 'form-control js-datetime',
                    'placeholder': 'дд.мм.гггг чч:мм',
                    'autocomplete': 'off',
                }
            ),
            'end_datetime': forms.DateTimeInput(
                format='%d.%m.%Y %H:%M',
                attrs={
                    'class': 'form-control js-datetime',
                    'placeholder': 'дд.мм.гггг чч:мм',
                    'autocomplete': 'off',
                }
            ),
            'ticket_price': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Напр. 25.00',
                    'step': '0.01',
                    'min': '0',
                    'max': '1000',
                }
            ),

            'venue': forms.Select(
                attrs={
                    'class': 'form-select',
                }
            ),
            'performers': forms.CheckboxSelectMultiple(
                attrs={
                    'class': 'form-check-input',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_datetime'].input_formats = [
            '%d.%m.%Y %H:%M',
            '%d.%m.%Y %H:%M:%S',
            '%Y-%m-%dT%H:%M',
            '%Y-%m-%d %H:%M:%S',
        ]
        self.fields['end_datetime'].input_formats = [
            '%d.%m.%Y %H:%M',
            '%d.%m.%Y %H:%M:%S',
            '%Y-%m-%dT%H:%M',
            '%Y-%m-%d %H:%M:%S',
        ]
        self.fields['venue'].empty_label = 'Изберете зала'

        if self.instance.pk:
            self.fields['status_display'] = forms.CharField(
                label='Статус',
                initial=self.instance.status_label,
                required=False,
                disabled=True,
                widget=forms.TextInput(
                    attrs={
                        'class': 'form-control',
                    }
                ),
            )

    def clean_title(self):

        title = self.cleaned_data.get('title', '').strip()
        if len(title) < 3:
            raise forms.ValidationError('Заглавието трябва да е поне 3 символа.')
        return title

    def clean_description(self):
        description = self.cleaned_data.get('description', '').strip()
        if len(description) > 1000:
            raise forms.ValidationError('Описанието не може да е над 1000 символа.')
        return description

    def clean_ticket_price(self):

        ticket_price = self.cleaned_data.get('ticket_price')
        if ticket_price is None:
            return ticket_price
        if ticket_price < 0:
            raise forms.ValidationError('Цената не може да е отрицателна.')
        if ticket_price > 1000:
            raise forms.ValidationError('Цената не може да е над 1000 €.')
        return ticket_price

    def clean_start_datetime(self):
        from django.utils import timezone

        start_datetime = self.cleaned_data.get('start_datetime')
        if start_datetime is None:
            return start_datetime

        today = timezone.localdate()
        if not self.instance.pk and start_datetime.date() < today:
            raise forms.ValidationError(
                'Началната дата не може да е преди днес.'
            )
        if (
            self.instance.pk
            and start_datetime.date() < today
            and start_datetime.date() != self.instance.start_datetime.date()
        ):
            raise forms.ValidationError(
                'Началната дата не може да е преди днес.'
            )
        return start_datetime

    def clean(self):
        cleaned_data = super().clean()
        start_datetime = cleaned_data.get('start_datetime')
        end_datetime = cleaned_data.get('end_datetime')
        performers = cleaned_data.get('performers')

        if start_datetime and end_datetime and end_datetime < start_datetime:
            self.add_error(
                'end_datetime',
                'Крайната дата трябва да е след или равна на началната.',
            )

        if start_datetime and end_datetime:
            duration = end_datetime - start_datetime
            if duration.days > 14:
                self.add_error(
                    'end_datetime',
                    'Събитието не може да продължава повече от 14 дни.',
                )

        if performers is not None and not performers.exists():
            self.add_error('performers', 'Моля, изберете поне един изпълнител.')

        return cleaned_data


class EventFilterForm(forms.Form):
    q = forms.CharField(
        required=False,
        label='Търсене',
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Търси по заглавие...',
            }
        ),
    )
    SORT_CHOICES = (
        ('', 'По подразбиране'),
        ('date_asc', 'Най-ранни първо'),
        ('date_desc', 'Най-късни първо'),
        ('title', 'Заглавие А-Я'),
        ('title_desc', 'Заглавие Я-А'),
    )

    sort = forms.ChoiceField(
        required=False,
        label='Сортиране',
        choices=SORT_CHOICES,
        widget=forms.HiddenInput(),
    )

    def clean_q(self):
        return self.cleaned_data.get('q', '').strip()
