from autocomplete_light import shortcuts as autocomplete_light
from teryt_tree.autocomplete_light_registry import (JednostkaAdministracyjnaAutocomplete,
                                                    CommunityAutocomplete)

from .models import JST


autocomplete_light.register(JST, JednostkaAdministracyjnaAutocomplete)
autocomplete_light.register(JST, CommunityAutocomplete)
