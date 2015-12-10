from django.views.generic import ListView
from foundation.letters.models import Letter


class HomeView(ListView):
    template_name = "home.html"
    model = Letter
    paginate_by = 25

    def get_queryset(self, *args, **kwargs):
        qs = super(HomeView, self).get_queryset(*args, **kwargs)
        qs = qs.for_milestone().order_by('-created')
        return qs
