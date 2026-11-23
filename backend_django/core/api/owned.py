"""Shared building blocks for user-owned REST resources.

Used by applications that expose per-user data (agents, crm, sales, revenue, ...).
Every queryset is scoped to the authenticated user and every related object that
a client submits is verified to belong to that same user, so one account can never
read, modify or link to another account's records.
"""

from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated


def _resolve_owner(obj, path):
    owner = obj
    for part in path.split("."):
        owner = getattr(owner, part, None)
        if owner is None:
            return None
    return owner


def ensure_owned(related, user, field, owner_path="user"):
    """Raise a field-level validation error unless ``related`` belongs to ``user``.

    ``related`` may be ``None`` (optional relation) and is then accepted.
    ``owner_path`` is the dotted attribute path from the related object to its
    owning user, e.g. ``"user"`` or ``"architecture.user"``.
    """
    if related is None:
        return related
    owner = _resolve_owner(related, owner_path)
    if owner is None or getattr(owner, "pk", None) != getattr(user, "pk", object()):
        raise ValidationError({field: "Select an item that belongs to your account."})
    return related


def ensure_all_owned(items, user, field, owner_path="user"):
    """Apply :func:`ensure_owned` to every element of a many-to-many selection."""
    for item in items or []:
        ensure_owned(item, user, field, owner_path)
    return items


def scope_related_fields(fields, user, mapping):
    """Limit the selectable objects of related fields to those owned by ``user``.

    ``mapping`` maps a serializer field name to the ORM lookup that reaches the
    owner (``{"contact": "user", "deal": "user"}``). This makes foreign and
    non-existent ids indistinguishable to the client (no id enumeration).
    """
    for name, lookup in mapping.items():
        field = fields.get(name)
        if field is None:
            continue
        target = getattr(field, "child_relation", field)
        queryset = getattr(target, "queryset", None)
        if queryset is not None:
            target.queryset = queryset.filter(**{lookup: user})


class OwnedModelViewSet(viewsets.ModelViewSet):
    """ModelViewSet limited to rows owned by ``request.user``.

    Subclasses set:

    * ``queryset_model`` - the model class,
    * ``owner_lookup`` - ORM path to the owning user (default ``"user"``),
    * ``set_owner_on_create`` - save ``user=request.user`` on create (default True),
    * ``filter_fields`` - query-string parameters that filter by exact value,
    * ``search_fields`` / ``ordering_fields`` - handled by DRF's built-in filters.
    """

    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    queryset_model = None
    owner_lookup = "user"
    set_owner_on_create = True
    filter_fields = ()
    select_related = ()

    def get_queryset(self):
        queryset = self.queryset_model.objects.filter(
            **{self.owner_lookup: self.request.user}
        )
        if self.select_related:
            queryset = queryset.select_related(*self.select_related)
        for name in self.filter_fields:
            value = self.request.query_params.get(name)
            if value in (None, ""):
                continue
            if value in ("true", "false"):
                value = value == "true"
            try:
                queryset = queryset.filter(**{name: value})
            except (ValueError, TypeError, DjangoValidationError):
                return queryset.none()
        return queryset

    def perform_create(self, serializer):
        if self.set_owner_on_create:
            serializer.save(user=self.request.user)
        else:
            serializer.save()
