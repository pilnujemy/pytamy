import autocomplete_light
from models import Contact

# This will generate a ContactAutocomplete class
autocomplete_light.register(Contact,
    search_fields=['name'],
)
