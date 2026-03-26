from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from buyer.models import CustomUser  # <-- use shared user model


class SellerSignupForm(UserCreationForm):

    username = forms.CharField(
        max_length=150,
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
    )
    first_name = forms.CharField(max_length=30, help_text="Optional.")
    last_name = forms.CharField(max_length=30, help_text="Optional.")
    email = forms.EmailField(
        max_length=254, help_text="Required. Enter a valid email address."
    )
    std_id = forms.CharField(
        max_length=20, help_text="Required. Enter your student ID."
    )
    shop_name = forms.CharField(
        max_length=100, help_text="Required. Enter your shop name."
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        help_text="Required. Enter a strong password.",
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput,
        help_text="Required. Enter the same password as before, for verification.",
    )

    class Meta:
        model = CustomUser  # <-- changed here
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "std_id",
            "shop_name",
            "password1",
            "password2",
        )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not (email.endswith("@std.ewubd.edu") or email.endswith("@ewubd.edu")):
            raise forms.ValidationError("Use EWU email only")
        return email


class SellerLoginForm(AuthenticationForm):
    username = forms.EmailField(
        max_length=254, help_text="Required. Enter a valid email address."
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        help_text="Required. Enter your password.",
    )
