from dal import autocomplete
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from UserDetails.models import User


class UserAPI(LoginRequiredMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # TODO: permissionchecks/ mixins, whatever

        print("Reached")

        qs = get_user_model().objects.all()

        if self.q:
            qs = qs.filter(
                Q(first_name__contains=self.q) |
                Q(last_name__contains=self.q) |
                Q(username__contains=self.q)
            )

        return qs