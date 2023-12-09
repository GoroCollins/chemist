import django_filters 

from . models import Item

from django.forms import forms

from django.contrib.auth.models import User

class ItemFilter(django_filters.FilterSet):
    code = django_filters.CharFilter(lookup_expr='icontains', widget=forms.TextInput(attrs={'class': 'form-control'}))
    created_by = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        empty_label="All Users",
        label="Users",
        widget=forms.Select(attrs={'class': 'form-control'}),
        )
    description = django_filters.CharFilter(lookup_expr='icontains', widget=forms.TextInput(attrs={'class': 'form-control'}))
    unit = django_filters.CharFilter(lookup_expr='exact', widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Item 
        fields = ['code', 'description', 'unit', 'created_by']