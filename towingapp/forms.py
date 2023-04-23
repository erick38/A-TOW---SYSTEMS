from django import forms
from towingapp.models import Message, Conversation, MyUser
from django.shortcuts import render,HttpResponseRedirect, get_object_or_404

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        conversation_id = self.data.get('conversation_id')
        conversation = get_object_or_404(Conversation, id=conversation_id, participants=self.user)
        cleaned_data['conversation'] = conversation
        cleaned_data['sender'] = self.user
        return cleaned_data

class ConversationForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea)

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.fields['participants'] = forms.ModelMultipleChoiceField(
            queryset=MyUser.objects.exclude(id=request.user.id),
            widget=forms.CheckboxSelectMultiple
    )
    def save(self):
        participants = list(self.cleaned_data['participants'])
        participants.append(self.request.user)  # add sender back to the list of participants
        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        message = Message.objects.create(
            conversation=conversation,
            sender=self.request.user,
            message=self.cleaned_data['message']
        )
        return conversation


class login_form(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class addclockinform(forms.Form):    
    STATUS_CHOICES = (
            ('clock-in', 'clock-in'),
            ('clock-out', 'clock-out'),
            )
    clock_status = forms.ChoiceField(choices=STATUS_CHOICES )

class add_AccountForm(forms.Form):
    username = forms.CharField(max_length=38)
    password = forms.CharField(widget=forms.PasswordInput)


# class AddmessageForm(forms.ModelForm):
#     recipient = forms.ModelChoiceField(queryset=get_user_model().objects.all())
#     message = forms.CharField(widget=forms.Textarea)

#     class Meta:
#         model = Mensaje
#         fields = ['recipient', 'message']

#     def __init__(self, sender, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['recipient'].label = 'Recipient'
#         self.fields['message'].label = 'Message'
#         self.fields['recipient'].queryset = get_user_model().objects.exclude(username=sender.username)
#         self.sender = sender

#     def save(self, commit=True):
#         mensaje = super().save(commit=False)
#         recipient = self.cleaned_data.get('recipient')
#         mensaje.recipient_url = mensaje.get_recipient_url(recipient)
#         if commit:
#             mensaje.save()
#         return mensaje