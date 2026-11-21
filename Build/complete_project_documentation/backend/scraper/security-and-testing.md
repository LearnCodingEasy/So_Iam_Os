# scraper security and testing

## Permission/ownership evidence

- scraper/api/views/scraper_views.py:L5: from rest_framework.permissions import IsAuthenticated
- scraper/api/views/scraper_views.py:L13: permission_classes = [IsAuthenticated]
- scraper/api/views/scraper_views.py:L15: def get_queryset(self):
- scraper/api/views/scraper_views.py:L16: qs = super().get_queryset()
- scraper/api/views/scraper_views.py:L17: user = self.request.user
- scraper/api/views/scraper_views.py:L27: permission_classes = [IsAuthenticated]
- scraper/api/views/scraper_views.py:L29: def get_queryset(self):
- scraper/api/views/scraper_views.py:L31: if self.request.user.is_staff:
- scraper/api/views/scraper_views.py:L33: return qs.filter(created_by=self.request.user)
- scraper/api/views/scraper_views.py:L36: serializer.save(created_by=self.request.user)
- scraper/api/views/scraper_views.py:L39: if serializer.instance.created_by_id != self.request.user.id and not self.request.user.is_staff:
- scraper/api/views/scraper_views.py:L45: if instance.created_by_id != self.request.user.id and not self.request.user.is_staff:
- scraper/api/views/scraper_views.py:L87: sources = self.get_queryset()
- scraper/api/views/scraper_views.py:L102: permission_classes = [IsAuthenticated]
- scraper/api/views/scraper_views.py:L105: if not self.request.user.is_staff and website.created_by_id != self.request.user.id:
- scraper/api/views/scraper_views.py:L112: if not self.request.user.is_staff and website.created_by_id != self.request.user.id:
- scraper/api/views/scraper_views.py:L117: def get_queryset(self):
- scraper/api/views/scraper_views.py:L119: if self.request.user.is_staff: return qs
- scraper/api/views/scraper_views.py:L120: return qs.filter(website__created_by=self.request.user)
- scraper/api/views/scraper_views.py:L125: permission_classes = [IsAuthenticated]
- scraper/api/views/scraper_views.py:L128: if not self.request.user.is_staff and parent.website.created_by_id != self.request.user.id:
- scraper/api/views/scraper_views.py:L135: if not self.request.user.is_staff and parent.website.created_by_id != self.request.user.id:
- scraper/api/views/scraper_views.py:L140: def get_queryset(self):
- scraper/api/views/scraper_views.py:L142: if self.request.user.is_staff: return qs
- scraper/api/views/scraper_views.py:L143: return qs.filter(parent__website__created_by=self.request.user)
- scraper/api/views/scraper_views.py:L148: permission_classes = [IsAuthenticated]
- scraper/api/views/scraper_views.py:L150: def get_queryset(self):
- scraper/api/views/scraper_views.py:L151: qs = super().get_queryset()
- scraper/api/views/scraper_views.py:L152: return qs if self.request.user.is_staff else qs.filter(website__created_by=self.request.user)


## Tests
- scraper/tests/test_scraper.py
- scraper/tests/__init__.py


Tests were not run. This scan is not a complete authorization/security review. Shared guidance: [authentication and permissions](../../07-authentication-and-permissions.md).
