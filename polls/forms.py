from django import forms
from .models import Question, Choice
from django.forms import modelformset_factory
from django.contrib.auth import authenticate, get_user_model
from datetimepicker.widgets import DateTimePicker


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('question_text',)


class QuestionModelForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('question_text',)
        labels = {
            'question_text': 'Question',
            }
        widgets = {
            'question_text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter question here'
                }),

        }


QuestionModelFormset = modelformset_factory(
    Question,
    fields=('question_text', ),
    extra=1,
    widgets={
        'question_text': forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Question here'
            }),
    }
)

ChoiceFormset = modelformset_factory(
    Choice,
    fields=('choice_text', ),
    extra=1,
    widgets={'choice_text': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter choice here'
        })
    }
)


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ('choice_text', )


User = get_user_model()


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("This user does not exist")
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect Password")
            if not user.is_active:
                raise forms.ValidationError("This user is no longer active")
        return super(UserLoginForm, self).clean(*args, **kwargs)



