from django import template

register = template.Library()


@register.simple_tag
def sort_link(request, column):
    req = request.GET.copy()
    if 'sort' not in req or req.get('sort', False) != column:
        req['sort'] = column
    else:
        req['sort'] = '-' + column
    return "?" + req.urlencode()
