from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic.list import ListView
from CreditManagement.models import *
from django.contrib import messages
from django.utils.translation import gettext as _
from .forms import UserTransactionForm, AssociationTransactionForm, UserDonationForm
from django.views.generic import View, TemplateView
from django.http import HttpResponseForbidden, HttpResponseRedirect, HttpResponse


class TransactionListView(ListView):
    template_name = "credit_management/history_credits.html"
    paginate_by = 10
    context_object_name = 'transactions'

    def get_queryset(self):
        return AbstractTransaction.get_all_transactions(user=self.request.user).order_by('-pk')


class TransactionAddView(LoginRequiredMixin, TemplateView):
    template_name = "credit_management/transaction_add.html"

    def get_context_data(self, **kwargs):
        context = super(TransactionAddView, self).get_context_data(**kwargs)
        association_name = self.kwargs.get('association_name')

        if association_name:
            association = Association.objects.get(slug=association_name)
            # If an association is given as the source, check user credentials
            if not self.request.user.is_board_of(association.id):
                return HttpResponseForbidden()
            # Create the form
            print(self.request.GET)
            context['form'] = AssociationTransactionForm(association, initial=self.request.GET, initial_from_get=True)
        else:
            context['form'] = UserTransactionForm(self.request.user, initial=self.request.GET, initial_from_get=True)

        return context

    def post(self, request, association_name=None):
        # Do form shenanigans
        print(request.POST)
        if association_name:
            association = Association.objects.get(slug=association_name)
            # If an association is given as the source, check user credentials
            if not request.user.is_board_of(association.id):
                return HttpResponseForbidden()
            # Create the form
            form = AssociationTransactionForm(association, data=request.POST)
        else:
            form = UserTransactionForm(request.user, data=request.POST)

        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, _("Transaction has been succesfully added."))
            return HttpResponseRedirect(request.path_info)

        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)


class DonationView(LoginRequiredMixin, TemplateView):
    template_name = "credit_management/transaction_add.html"
    context = {}

    def get_context_data(self, **kwargs):
        context = super(DonationView, self).get_context_data(**kwargs)
        context['form'] = UserDonationForm(self.request.user, initial=self.request.GET, initial_from_get=True)
        return context

    def post(self, request):
        form = UserDonationForm(request.user, request.POST)

        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, _("Transaction has been succesfully added."))
            return HttpResponseRedirect(request.path_info)

        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)


class AssociationTransactionListView:
    pass


class UserTransactionListView(ListView):
    pass


class TransactionFinalisationView(View):
    context = {}
    template_name = "credit_management/transaction_finalise.html"

    def get(self, request):
        return render(request, self.template_name, self.context)

    def post(self, request):
        self.context['transactions'] = AbstractPendingTransaction.finalise_all_expired()

        return render(request, self.template_name, self.context)


class MoneyObtainmentView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        from django.db.models import Q, Count

        # Only superusers can access this page
        if not request.user.is_superuser:
            return HttpResponseForbidden
        # Todo: allow access by permission
        # Todo: linkin in interface

        # Get the end date

        # Filter on end date
        date_end = request.GET.get('to', None)
        if date_end:
            date_end = datetime.strptime(date_end, '%d/%m/%y')
        else:
            date_end = timezone.now()

        # Filter on a start date
        date_start = request.GET.get('from', None)
        if date_start:
            date_start = datetime.strptime(date_start, '%d/%m/%y')
        else:
            date_start = date_end

        # Get all fixed transactions in the date range
        transactions = FixedTransaction.objects. \
            filter(confirm_moment__gte=date_start,
                   confirm_moment__lte=date_end)
        # Aggregate the values
        from django.db.models import Sum
        amount_in = transactions.filter(target_user__isnull=True,
                                        target_association__isnull=True).aggregate(sum=Sum('amount'))

        amount_out = transactions.filter(source_user__isnull=True,
                                         source_association__isnull=True).aggregate(sum=Sum('amount'))

        # Create the response
        message = "Time from {date_start} to {date_end}:<br>In: {amount_in}<br>Out: {amount_out}"
        message = message.format(date_start=date_start, date_end=date_end,
                                 amount_in=amount_in['sum'], amount_out=amount_out['sum'])

        # Return the respnonse
        return HttpResponse(message)
