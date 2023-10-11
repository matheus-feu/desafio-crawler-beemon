from django import forms

from app.tasks import send_feedback_email_task


class URLScrappyForm(forms.Form):
    url = forms.URLField(label='URL to Scrape', max_length=200)

    class Meta:
        fields = "__all__"


class FeedbackForm(forms.Form):
    name = forms.CharField(
        label='Nome',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}))

    email = forms.EmailField(
        label='Email',
        max_length=100,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'required': 'true'}))

    message = forms.CharField(
        label='Mensagem',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'required': 'true'}))

    def send_email(self):
        send_feedback_email_task.delay(
            self.cleaned_data["name"],
            self.cleaned_data["email"],
            self.cleaned_data["message"],
        )

    class Meta:
        fields = "__all__"
