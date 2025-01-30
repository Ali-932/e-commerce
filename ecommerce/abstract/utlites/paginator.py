from math import ceil

from django.core.paginator import Paginator, EmptyPage


class CustomPaginator(Paginator):
    def validate_number(self, number):
        try:
            return super().validate_number(number)
        except EmptyPage:
            if int(number) > 1:
                # return the last page
                return self.num_pages
            elif int(number) < 1:
                # return the first page
                return 1
            else:
                raise


def paginated_response(queryset, per_page=10, page=1, *args):
    try:
        total_count = queryset.count()
    except TypeError:
        total_count = 1
    limit = per_page
    offset = per_page * (page - 1)
    page_count = ceil(total_count / per_page)

    return {
        'total_count': total_count,
        'per_page': limit,
        'from_record': offset + 1,
        'to_record': (offset + limit)
        if (offset + limit) <= total_count
        else (total_count % per_page) + offset,
        'has_previous': page > 1,
        'has_next': page < page_count,
        'previous_page': page - 1 if page > 2 else 1,
        'current_page': page,
        'next_page': min(page + 1, page_count),
        'page_count': page_count,
        'page_range': range(1, page_count + 1),
    }
