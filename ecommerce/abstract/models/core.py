from itertools import chain

from django.db import models

# Create your models here.

from django.db import models
from django_currentuser.db.models import CurrentUserField
from taggit.managers import TaggableManager


class IntEntity(models.Model):
    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    updated_at = models.DateTimeField(editable=False, auto_now=True)
    extra = models.JSONField(null=True, blank=True, default=dict)

    tags = TaggableManager()

    created_by = CurrentUserField(related_name="%(app_label)s_%(class)s_adder")
    updated_by = CurrentUserField(on_update=True, related_name="%(app_label)s_%(class)s_updater")

    def to_dict(self, fields=None, exclude=None):
        """
        Return a dict containing the data in ``instance`` suitable for passing as
        a Form's ``initial`` keyword argument.

        ``fields`` is an optional list of field names. If provided, return only the
        named.

        ``exclude`` is an optional list of field names. If provided, exclude the
        named from the returned dict, even if they are listed in the ``fields``
        argument.
        """
        opts = self._meta
        data = {}
        for f in chain(
                opts.concrete_fields,
                # opts.private_fields,
                # opts.many_to_many
        ):
            if not getattr(f, 'editable', False):
                continue
            if fields is not None and f.name not in fields:
                continue
            if exclude and f.name in exclude:
                continue
            data[f.name] = f.value_from_object(self)
        return data

