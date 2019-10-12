from dal_select2.widgets import ModelSelect2
from django import forms
from django.core.exceptions import ValidationError

from CreditManagement.models import PendingTransaction


class TransactionForm(forms.ModelForm):
    origin = forms.CharField(disabled=True)

    def __init__(self, *args, user=None, association=None, **kwargs):
        super().__init__(*args, **kwargs)

        # Set the transaction source
        if user:
            self.instance.source_user = user
            self.fields['origin'].initial = user
        elif association:
            self.instance.source_association = association
            self.fields['origin'].initial = association
        else:
            raise ValueError("source is neither user nor association")

    class Meta:
        model = PendingTransaction
        fields = ['origin', 'amount', 'target_user', 'target_association']
        widgets = {
            'target_user': ModelSelect2(url='people_autocomplete', attrs={'data-minimum-input-length': '1'}),
        }


class AssociationTransactionForm(TransactionForm):

    def __init__(self, association, *args, **kwargs):
        super().__init__(*args, association=association, **kwargs)
        self.fields['target_user'].required = True

    class Meta(TransactionForm.Meta):
        fields = ['origin', 'amount', 'target_user', 'description']
        labels = {
            'target_user': 'User',
        }


class UserTransactionForm(TransactionForm):

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, user=user, **kwargs)
        self.fields['target_user'].required = False
        self.fields['target_association'].required = False

    class Meta(TransactionForm.Meta):
        fields = ['origin', 'amount', 'target_user', 'target_association', 'description']

    def clean(self):
        cleaned_data = super().clean()

        # Do not allow associations to make evaporating money transactons
        # (not restircted on database level, but it doesn't make sense to order it)
        if not cleaned_data.get('target_user') and not cleaned_data.get('target_association'):
            raise ValidationError("Select a target to transfer the money to.")

        return cleaned_data
