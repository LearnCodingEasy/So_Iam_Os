# Project Name

## Github

- [Github](./Learn_Github/index.md)

---

## LICENSE

- [LICENSE](Learn_License/index.md)

---

## Vite Press

- [Vite Press](Learn_Vite_Press/index.md)

---

## Django

- [Django](Learn_Django/index.md)

### 🔧 Django

```cmd
pip install python-decouple
```

```cmd
pip install lxml
```

```cmd
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

```cmd
pip install playwright celery redis
```

```cmd
playwright install
```

```cmd
pip install playwright
```

```cmd
pip install gspread oauth2client
```

```cmd
pip install rich
```

### 🕸️ scraper

#### 📝 [ models.py ]

- يمثل موقع إلكتروني واحد هتسحب منه البيانات.

- كل موقع ليه اسم + رابط رئيسي + وصف + حالة التفعيل.

```python
from django.db import models
from django.contrib.auth.models import User
import json

class Website(models.Model):
    name = models.CharField(max_length=200)
    base_url = models.URLField()
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

```

- بيمثل إعدادات السحب (scraping) لموقع معين.

- بيقولك هتسحب إيه، و منين، و إزاي.

- Meta يعني ما ينفعش يكون في موقع عنده نفس field_name مرتين.

```python
class ScrapingConfig(models.Model):
    SELECTOR_TYPES = [
        ('css', 'CSS Selector'),
        ('xpath', 'XPath'),
    ]

    website = models.ForeignKey(
        Website, on_delete=models.CASCADE, related_name='configs')
    # e.g., 'product_name', 'price', 'description'
    field_name = models.CharField(max_length=100)
    selector = models.TextField()  # The actual CSS selector or XPath
    selector_type = models.CharField(
        max_length=10, choices=SELECTOR_TYPES, default='css')
    is_required = models.BooleanField(default=True)
    # text, number, url, etc.
    data_type = models.CharField(max_length=50, default='text')

    class Meta:
        unique_together = ['website', 'field_name']

    def __str__(self):
        return f"{self.website.name} - {self.field_name}"

```

- كل مهمة (Job) بتمثل محاولة لسحب البيانات من موقع معين.

- بترصد الحالة (pending - running - completed - failed)

```python
class ScrapingJob(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    website = models.ForeignKey(Website, on_delete=models.CASCADE)
    target_url = models.URLField()
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    items_scraped = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.website.name} - {self.started_at.strftime('%Y-%m-%d %H:%M')}"

```

- بيمثل عنصر بيانات تم سحبه في نتيجة Job معينة.

- بيتخزن كـ JSON.

```python
class ScrapedData(models.Model):
    job = models.ForeignKey(
        ScrapingJob, on_delete=models.CASCADE, related_name='scraped_items')
    data = models.JSONField()  # Stores the actual scraped data as JSON
    scraped_at = models.DateTimeField(auto_now_add=True)
    source_url = models.URLField()  # The specific page this data came from

    def __str__(self):
        return f"Data from {self.job.website.name} - {self.scraped_at}"

```

#### 📝 [ views.py ]

- API للتحكم في المواقع (Website) – تقدر تعمل:

- إنشاء موقع

- تعديل

- حذف

- عرض الكل

- عرض واحد

```python
class WebsiteViewSet(viewsets.ModelViewSet):
    queryset = Website.objects.all().order_by(
        '-created_at')

    serializer_class = WebsiteSerializer

    @action(detail=True, methods=['get'])
    def configs(self, request, pk=None):
        """Get all scraping configurations for a website"""
        website = self.get_object()
        configs = website.configs.all()
        serializer = ScrapingConfigSerializer(configs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def jobs(self, request, pk=None):
        """Get all scraping jobs for a website"""
        website = self.get_object()
        jobs = website.scrapingjob_set.all().order_by('-started_at')
        serializer = ScrapingJobSerializer(jobs, many=True)
        return Response(serializer.data)

```

- بيرجع كل إعدادات السحب (ScrapingConfig) الخاصة بالموقع ده.

```python
class ScrapingConfigViewSet(viewsets.ModelViewSet):
    serializer_class = ScrapingConfigSerializer

    def get_queryset(self):
        website_id = self.request.query_params.get('website', None)
        if website_id:
            return ScrapingConfig.objects.filter(website_id=website_id)
        return ScrapingConfig.objects.all()

```

- بيرجع كل مهام السحب (ScrapingJob) الخاصة بالموقع ده.

```python

class ScrapingJobViewSet(viewsets.ModelViewSet):
    queryset = ScrapingJob.objects.all().order_by('-started_at')
    serializer_class = ScrapingJobSerializer

    @action(detail=False, methods=['post'])
    def start_scraping(self, request):
        """Start a new scraping job"""
        website_id = request.data.get('website_id')
        target_url = request.data.get('target_url')

        if not website_id or not target_url:
            return Response(
                {'error': 'website_id and target_url are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        website = get_object_or_404(Website, id=website_id)

        # Create the job
        job = ScrapingJob.objects.create(
            website=website,
            target_url=target_url,
            status='pending'
        )

        # TODO: In Step 4, we'll add the actual scraping logic here
        # For now, just return the created job
        serializer = ScrapingJobSerializer(job)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def results(self, request, pk=None):
        """Get scraped data for a specific job"""
        job = self.get_object()
        scraped_data = job.scraped_items.all()
        serializer = ScrapedDataSerializer(scraped_data, many=True)
        return Response(serializer.data)

```

---

---

---

---
