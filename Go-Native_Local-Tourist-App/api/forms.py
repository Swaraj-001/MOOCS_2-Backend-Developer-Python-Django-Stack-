from django import forms 


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    email = forms.CharField(max_length = 200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'})) 
    password = forms.CharField(widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})) 

class LoginForm(forms.Form): 
    email = forms.CharField(max_length = 200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'})) 
    password = forms.CharField(widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


CITY = {
    ("Hyderabad","Hyderabad"),
    ("Mumbai","Mumbai"),
}

class NewMonumentForm(forms.Form): 
    title = forms.CharField(max_length = 200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'})) 
    bannerImg = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    description = forms.CharField(widget = forms.Textarea(attrs={'class': 'form-control', 'style':"height: 100px", 'placeholder': 'Password'}))
    city = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    address = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    otherThings = forms.CharField(widget = forms.Textarea(attrs={'class': 'form-control', 'style':"height: 100px", 'placeholder': 'Password'}))


class AddMonumentImgForm(forms.Form):
    image = forms.CharField( widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Image'})) 

class SearchForm(forms.Form):
    search = forms.CharField( widget=forms.TextInput(attrs={'class': 'search_input', 'placeholder': 'Location'})) 
    