from django import template

register = template.Library()


@register.filter
def price_label(value):
    try:
        price = float(value)
    except (TypeError, ValueError):
        return value

    if price == 0:
        return 'Безплатно'

    return f'{price:.2f} лв.'


@register.simple_tag(takes_context=True)
def active_link(context, *url_names):
    request = context.get('request')
    if request is None or request.resolver_match is None:
        return ''

    current_name = request.resolver_match.url_name
    if current_name in url_names:
        return 'active'

    return ''