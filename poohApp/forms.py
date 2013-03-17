__author__ = 'mengmeng'
from django import forms as forms

TOPIC_CHOICES = (
    ('general', 'General enquiry'),
    ('bug', 'Bug report'),
    ('suggestion', 'Suggestion'),
)

class RegisterForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()
    gender = forms.CharField()

class LoginForm(forms.Form):
    login_email = forms.EmailField(max_length=128)
    login_password = forms.CharField(min_length=6)
    remember_me = forms.CharField(required=False)

class ContactForm(forms.Form):
    # subject = forms.ChoiceField(choices=TOPIC_CHOICES)
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea())
    from_email = forms.EmailField(required=False,label='Your e-mail address')
    # def clean_message(self):
    #     message = self.cleaned_data.get('message', '')
    #     num_words = len(message.split())
    #     if num_words < 4:
    #         raise forms.ValidationError("Not enough words!")
    #     return message

class CommentForm(forms.Form):

    def __init__(self, object, *args, **kwargs):
        """Override the default to store the original document
        that comments are embedded in.
        """
        self.object = object
        return super(CommentForm, self).__init__(*args, **kwargs)

    def save(self, *args):
        """Append to the comments list and save the post"""
        self.object.comments.append(self.instance)
        self.object.save()
        return self.object

