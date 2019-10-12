from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.forms import ModelForm
from django.utils import timezone

from Dining.models import UserDiningSettings
from .models import Association, User, UserMembership


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email')


class RegisterUserDetails(forms.ModelForm):
    first_name = forms.CharField(max_length=40, required=True)
    last_name = forms.CharField(max_length=40, required=True)
    allergies = forms.CharField(max_length=100, required=False, help_text="Max 100 characters, leave empty if none")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'allergies']

    def save_as(self, user):
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.userdiningsettings.allergies = self.cleaned_data.get('allergies')
        user.save()
        user.userdiningsettings.save()


class DiningProfileForm(ModelForm):
    class Meta:
        model = UserDiningSettings
        fields = ['allergies']


class UserForm(ModelForm):
    name = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ['username', 'name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].disabled = True
        self.fields['name'].initial = str(self.instance)
        self.fields['email'].disabled = True


class AssociationLinkField(forms.BooleanField):
    """A special BooleanField model for association links.

    Can also indicate current validation state and auto-sets initial value
    """

    def __init__(self, user, association, *args, **kwargs):
        super(AssociationLinkField, self).__init__(*args, **kwargs)

        self.initial = False
        self.required = False
        self.label = association.name
        self.user = user
        self.association = association
        self.membership = None

        # Find the membership, if any
        if user is not None:
            try:
                self.membership = association.usermembership_set.get(related_user=user)
                self.initial = self.membership.is_member()
                if self.membership.get_verified_state() is None:
                    self.pending = True

                # Check how recently the member has been verified or not. If too recent, block change
                if self.membership.verified_on is not None:
                    if self.membership.is_verified:
                        if self.membership.verified_on + \
                                settings.DURATION_AFTER_MEMBERSHIP_CONFIRMATION > timezone.now():
                            # The user has been verified to recently (prevent spamming)
                            self.disabled = True
                    else:
                        if self.membership.verified_on + \
                                settings.DURATION_AFTER_MEMBERSHIP_REJECTION > timezone.now():
                            # The user has been verified not to be a member to recently (prevent spamming)
                            self.disabled = True

            except UserMembership.DoesNotExist:
                pass
        if association is None:
            raise ValueError("Association can not be None")

    def verified(self):
        if self.membership is None:
            return None
        return self.membership.get_verified_state()

    def get_membership_model(self, user=None, new_value=True):
        # Check input data for correctness
        if self.user is None and user is None:
            raise ValueError("Field does not contain user and user was not given in method")
        if user is not None and self.user is not None and self.user != user:
            raise ValueError("Given user differs from field user")

        if self.membership is not None:
            return self.membership
        if self.user is not None:
            # If there was a user given, but the link was not found. Create a new link if allowed
            if new_value:
                return UserMembership(related_user=self.user, association=self.association)
        else:
            # user originally not given. Try to find the link
            try:
                return self.association.usermembership_set.get(related_user=user)
            except UserMembership.DoesNotExist:
                if new_value:
                    return UserMembership(related_user=user, association=self.association)
        return None


class AssociationLinkForm(forms.Form):

    def __init__(self, user, *args, **kwargs):
        super(AssociationLinkForm, self).__init__(*args, **kwargs)

        self.user = user

        if user is None:
            associations = Association.objects.filter(is_choosable=True)
        else:
            associations = Association.objects.filter(Q(is_choosable=True) | (Q(is_choosable=False) & Q(
                usermembership__related_user=user))).order_by('slug')

        # Get all associations and make a checkbox field
        for association in associations:
            field = AssociationLinkField(user, association)
            # (using the slug since HTML IDs may not contain spaces)
            self.fields[association.slug] = field

    def clean(self):
        cleaned_data = super().clean()
        # Check if user is assigned to at least one association
        has_association = True in self.cleaned_data.values()

        if not has_association:
            raise ValidationError("At least one association needs to be chosen")

        return cleaned_data

    def save(self, user=None):
        """Saves the association links by creating or removing UserMembership instances."""
        if not self.user and not user:
            raise ValueError("Both self.user and user are None")
        if user is None:
            user = self.user

        for key, value in self.cleaned_data.items():
            link = self.fields[key].get_membership_model(user, new_value=value)
            if value:
                if link.id is None:
                    link.save()
                elif link.get_verified_state() is False:
                    # If user was rejected, and a new request is entered
                    link.verified_on = None
                    link.save()
            else:
                if link and link.get_verified_state() is not False:
                    link.delete()


class AssociationSettingsForm(forms.ModelForm):
    class Meta:
        model = Association
        fields = ['balance_update_instructions']
