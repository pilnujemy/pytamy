from django.views.generic import TemplateView
from foundation.letters.models import Letter


class HomeView(TemplateView):
    template_name = "home.html"
    inbox_select_related = ['case', 'author', 'sender_user', 'sender_office']

    def get_context_data(self, *args, **kwargs):
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context['inbox'] = (Letter.objects.select_related(*self.inbox_select_related).
                            order_by('-created').all()[:20])
        return context
