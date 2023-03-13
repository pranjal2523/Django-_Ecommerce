from django.forms import ModelForm
from .models import BillAdd

class Billform(ModelForm):
    class Meta:
        model = BillAdd
        fields = ('address','zipcode', 'city', 'contry',)