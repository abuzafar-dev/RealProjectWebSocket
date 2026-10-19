from django import forms
from django.utils.text import slugify

from chat.models import Room


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Yangi xona nomi'}),
        }
        labels = {'name': ''}

    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        slug = slugify(name)
        if not slug:
            raise forms.ValidationError('Xona nomida lotin harf yoki raqam bo\'lishi kerak')
        if Room.objects.filter(slug=slug).exists():
            raise forms.ValidationError('Bunday xona allaqachon bor')
        return name

    def save(self, commit=True):
        room = super().save(commit=False)
        room.slug = slugify(room.name)
        if commit:
            room.save()
        return room
