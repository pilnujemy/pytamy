from django.views.generic import TemplateView
from foundation.letters.models import Letter


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, *args, **kwargs):
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context['inbox'] = Letter.objects.all()[:20]
        return context
