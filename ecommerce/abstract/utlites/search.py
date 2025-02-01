import contextlib
import operator
from datetime import datetime
from functools import reduce

from django.core.exceptions import FieldDoesNotExist
from django.db.models import Q
from django.utils import timezone
from django.utils.text import smart_split, unescape_string_literal


from functools import reduce
import operator
from django.db.models import Q, Value, IntegerField, Case, When

def get_search_results(qs, search_fields, search_term):
    """
    Filters the queryset by search_term on provided search_fields and
    annotates with a score that reflects how well each row matches the search.
    Orders results by the score in descending order.
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
        prev_field = None
        for path_part in lookup_fields:
            if path_part == 'pk':
                path_part = opts.pk.name
            try:
                field = opts.get_field(path_part)
            except Exception:
                # In case the field lookup fails, return the lookup as-is.
                if prev_field and prev_field.get_lookup(path_part):
                    return field_name
            else:
                prev_field = field
                if hasattr(field, 'get_path_info'):
                    opts = field.get_path_info()[-1].to_opts
        return f"{field_name}__icontains"

    # Only proceed if both search_fields and search_term are provided.
    if search_fields and search_term:
        # Prepare lookup expressions from each search_field.
        orm_lookups = [construct_search(str(field)) for field in search_fields]

        # Split the search_term into bits.
        # (Assuming smart_split and unescape_string_literal are defined elsewhere.)
        # gives a generator (demon, slayer)
        search_bits = smart_split(search_term)

        # Build the Q filter: for each bit, match any of the field lookups.
        combined_q = Q()
        for bit in search_bits:
            if bit.startswith(('"', "'")) and bit[0] == bit[-1]:
                bit = unescape_string_literal(bit)
            # For this search token, create a disjunction across all lookups.
            sub_q = reduce(operator.or_, (Q(**{lookup: bit}) for lookup in orm_lookups))
            combined_q |= sub_q
        # Filter the queryset.
        qs = qs.filter(combined_q).distinct()

        # Build a list of score contributions. For every lookup & token combination,
        # if the condition matches then add a point (or more, if you want weighting).
        score_cases = []
        for lookup in orm_lookups:
            score_cases.append(
                Case(
                    When(**{lookup: search_term}, then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField()
                )
            )
        # Sum the score contributions.
        # We use reduce to add up the cases; starting with 0.
        total_score = reduce(operator.add, score_cases, Value(0))
        qs = qs.annotate(ft_score=total_score)
        qs = qs.order_by('-ft_score')

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

