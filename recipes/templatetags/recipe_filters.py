from django import template

register = template.Library()


@register.filter()
def addclass(field, css):
    return field.as_widget(attrs={'class': css})


@register.filter
def get_tag_filter(value):
    return value.getlist('filters')


@register.filter
def get_filter_link(request, tag):
    new_request = request.GET.copy()

    if tag.title in request.GET.getlist('filters'):
        tags = new_request.getlist('filters')
        tags.remove(tag.title)
        new_request.setlist('filters', tags)
    else:
        new_request.appendlist('filters', tag.title)

    return new_request.urlencode()
