from django import forms
from django.forms import ModelForm
from .models import Post

from django import forms
from django.forms import SelectDateWidget
from django.utils import timezone
from .models import Post


class TimePickerWidget(forms.TextInput):
    input_type = 'time'


class PostForm(forms.ModelForm):
    training_date = forms.DateField(
        label='Дата', widget=SelectDateWidget(), initial=timezone.now().date())
    training_time = forms.TimeField(
        label='Время', widget=TimePickerWidget(), initial=timezone.now().time())

    class Meta:
        model = Post
        fields = ['title', 'court', 'training_date',
                  'training_time', 'preferences']
