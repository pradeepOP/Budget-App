from django.forms import ModelForm
from .models import Transaction
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ["amount", "category", "description", "is_income"]

    def __init__(self, *args, **kwargs):
        prev_budget = kwargs.pop('prev_budget', None)
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.budget = prev_budget

        self.fields["category"].widget.attrs.update({"class": "rounded-lg"})
        self.fields["amount"].widget.attrs.update(
            {"class": "outline-none rounded-lg w-full",
                "placeholder": "Enter amount", "name": "amount"}
        )
        self.fields["description"].widget.attrs.update(
            {
                "class": "outline-none rounded-lg w-full tracking-wider",
                "placeholder": "Enter description of transaction......",
            }
        )

    def clean(self):
        cleaned_data = super().clean()
        is_income = cleaned_data.get('is_income')
        amount = cleaned_data.get('amount')

        amount = amount if is_income else -amount

        if self.budget + amount < 0:
            self.add_error("amount", 'Budget cannot be negative')


class signUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email",
                  "username", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super(signUpForm, self).__init__(*args, **kwargs)

        self.fields["first_name"].widget.attrs.update(
            {"class": "rounded-lg w-full"})
        self.fields["last_name"].widget.attrs.update(
            {"class": "rounded-lg w-full"})
        self.fields["email"].widget.attrs.update(
            {"class": "rounded-lg w-full"})
        self.fields["username"].widget.attrs.update(
            {"class": "rounded-lg w-full"})
        self.fields["password1"].widget.attrs.update(
            {"class": "rounded-lg w-full"})
        self.fields["password2"].widget.attrs.update(
            {"class": "rounded-lg w-full"})

    def clean(self):
        clean_data = super().clean()

        password1 = clean_data.get('password1')
        password2 = clean_data.get('password2')

        if password1 != password2:
            self.add_error('password1', 'password didnot match')
