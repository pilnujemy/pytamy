from teryt_tree.models import JednostkaAdministracyjna
from django.core.urlresolvers import reverse
from cached_property import cached_property


class JST(JednostkaAdministracyjna):

    @cached_property
    def get_offices_in_region(self):
        Office = self.office_set.model
        return Office.objects.area(self)

    def get_absolute_url(self):
        if self.level == 0:
            return reverse('teryt:details_w', kwargs={'slug': self.slug})
        if self.level == 1:
            return reverse('teryt:details_p', kwargs={'slug': self.slug})
        if self.level == 2:
            return reverse('teryt:details_g', kwargs={'slug': self.slug})
        return reverse('teryt:details', kwargs={'slug': self.slug})

    class Meta:
        proxy = True
