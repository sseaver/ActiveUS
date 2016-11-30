from django import forms
from django.core.mail import send_mail
from app.models import Event, Team


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
        recipient_list = ["activeus321@gmail.com"]
        send_mail(subject, body, "do_not_reply@ActiveUS.com", recipient_list)


class ContactUserForm(forms.Form):
    sender = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)
    recipient = forms.CharField()

    def send_email(self):
        sender = self.cleaned_data["sender"]
        message = self.cleaned_data["message"]
        recipient = self.cleaned_data["recipient"]
        subject = "Message from another ActiveUS user"
        body = """
        Sent from ActiveUS.
        From: {}
        Message: {}
        """.format(sender, message)
        recipient_list = [recipient]
        send_mail(subject, body, "do_not_reply@ActiveUS.com", recipient_list)


class MultiContactEmailForm(forms.Form):
    sender = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self, id):
        recipient_list = []
        for player in Team.objects.get(id=id).players.all():
            recipient_list.append(player.profile.email)
        sender = self.cleaned_data["sender"]
        message = self.cleaned_data["message"]
        subject = "Message from ActiveUS team"
        body = """
        Sent from ActiveUS.
        From: {}
        Message: {}
        """.format(sender, message)
        recipient_list = recipient_list
        send_mail(subject, body, "do_not_reply@ActiveUS.com", recipient_list)


# class EventParticipantsEmailForm(forms.Form):
#     sender = forms.CharField()
#     message = forms.CharField(widget=forms.Textarea)
#
#     def send_email(self, id):
#         recipient_list = []
#         if not Event.objects.get(id=id).team:
#             for player in Event.objects.get(id=id).participants.all():
#                 recipient_list.append(player.profile.email)
#         else:
#             for team in Event.objects.get(id=id).team.all():
#                 for player in team:
#                     recipient_list.append(player.profile.email)
#         sender = self.cleaned_data["sender"]
#         message = self.cleaned_data["message"]
#         subject = "Message from ActiveUS team"
#         body = """
#         Sent from ActiveUS.
#         From: {}
#         Message: {}
#         """.format(sender, message)
#         recipient_list = recipient_list
#         send_mail(subject, body, "do_not_reply@ActiveUS.com", recipient_list)
#

class CreateEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ("name", "description", "sport", "date", "time", "location", "participants", "visibility", "team")

    def __init__(self, *args, user=None, **kwargs):
        super(CreateEventForm, self).__init__(*args, **kwargs)
        self.fields['team'].queryset = user.team_set.all()
