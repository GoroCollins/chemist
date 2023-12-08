import django_filters 

from . models import Item

from django.forms import forms

from django.contrib.auth.models import User

class ItemFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    created_by = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        empty_label="All Users",
        label="Users",
        widget=forms.Select(attrs={'class': 'form-control'}),
        )
    
    class Meta:
        model = Item 
        fields = ['code', 'description', 'unit', 'created_by']