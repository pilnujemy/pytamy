from __future__ import absolute_import
from .. import models
from teryt_tree.factories import JednostkaAdministracyjnaFactory


class JSTFactory(JednostkaAdministracyjnaFactory):
    class Meta:
        model = models.JST
