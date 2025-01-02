import contextlib
import operator
from datetime import datetime
from functools import reduce

from django.core.exceptions import FieldDoesNotExist
from django.db.models import Q
from django.utils import timezone
from django.utils.text import smart_split, unescape_string_literal


def get_search_results(qs, search_fields, search_term):
    """
    It takes a queryset, a list of search fields, and a search term, and returns a queryset that is filtered by the search
    term

    :param qs: The queryset to filter
    :param search_fields: A list of fields to search
    :param search_term: The search term entered by the user
    :return: A queryset
    """

    def construct_search(field_name):
        if field_name.startswith('^'):
            return f"{field_name[1:]}__istartswith"
        elif field_name.startswith('='):
            return f"{field_name[1:]}__iexact"
        elif field_name.startswith('@'):
            return f"{field_name[1:]}__search"
        opts = qs.model._meta
        lookup_fields = field_name.split('__')
        # Go through the fields, following all relations.
        prev_field = None
        for path_part in lookup_fields:
            if path_part == 'pk':
                path_part = opts.pk.name
            try:
                field = opts.get_field(path_part)
            except FieldDoesNotExist:
                # Use valid query lookups.
                if prev_field and prev_field.get_lookup(path_part):
                    return field_name
            else:
                prev_field = field
                if hasattr(field, 'get_path_info'):
                    # Update opts to follow the relation.
                    opts = field.get_path_info()[-1].to_opts
        # Otherwise, use the field with icontains.
        return f"{field_name}__icontains"

    if search_fields and search_term:
        orm_lookups = [construct_search(str(search_field))
                       for search_field in search_fields]
        or_queries=[]
        for bit in smart_split(search_term):
            if bit.startswith(('"', "'")) and bit[0] == bit[-1]:
                bit = unescape_string_literal(bit)
            or_queries.extend([Q(**{orm_lookup: bit})
                          for orm_lookup in orm_lookups])
            qs = qs.filter(reduce(operator.or_, or_queries))

    return qs




def clean_search_dates(request):
    q = request.GET.get('q')
    today_str = f'{timezone.now().year}-{timezone.now().month}-{timezone.now().day}'
    date_from = request.GET.get('date_from', today_str)
    date_to = request.GET.get('date_to', today_str)

    with contextlib.suppress(Exception):
        date_from = datetime.strptime(f'{date_from} 00:00', '%Y-%m-%d %H:%M')
        date_to = datetime.strptime(f'{date_to} 23:59', '%Y-%m-%d %H:%M')
    return q, date_from, date_to

