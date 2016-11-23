from django import forms
from django.core.mail import send_mail


class ContactUsForm(forms.Form):
    sender = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self):
        sender = self.cleaned_data["sender"]
        message = self.cleaned_data["message"]
        subject = "ActiveUS Contact Form"
        body = """
        Sent from ActiveUS contact page.
        From: {}
        Message: {}
        """.format(sender, message)
        recipient_list = ["sseaver321@gmail.com"]
        send_mail(subject, body, "do_not_reply@ActiveUS.com", recipient_list)
