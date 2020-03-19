from django.forms import ModelForm
from c2shiptrack.models import *
from django.contrib.auth.models import User

class LokasiForm(ModelForm):
    class Meta:
        model = Lokasi
        fields = "__all__"

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password', )

class LokasiUserForm(ModelForm):
    class Meta:
        model = LokasiUser
        fields = ('nama', 'lokasi', )



