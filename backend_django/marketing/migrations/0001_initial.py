# Hand-written initial migration (Django was not available to run makemigrations).
# Field definitions mirror the models exactly; verify with
#   python manage.py makemigrations --check --dry-run

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('crm', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MarketingChannel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.CASCADE, related_name='marketing_channels')),
                ('name', models.CharField(max_length=160)),
                ('channel_type', models.CharField(max_length=20, choices=[('social', 'Social'), ('email', 'Email'), ('content', 'Content'), ('ads', 'Ads'), ('event', 'Event'), ('referral', 'Referral'), ('other', 'Other')], default='social')),
                ('url', models.URLField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['name']},
        ),
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.CASCADE, related_name='marketing_campaigns')),
                ('channel', models.ForeignKey('marketing.marketingchannel', null=True, blank=True, on_delete=django.db.models.deletion.SET_NULL, related_name='campaigns')),
                ('name', models.CharField(max_length=200)),
                ('objective', models.TextField(blank=True)),
                ('status', models.CharField(max_length=20, choices=[('draft', 'Draft'), ('scheduled', 'Scheduled'), ('running', 'Running'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='draft')),
                ('budget', models.DecimalField(max_digits=14, decimal_places=2, default=0)),
                ('spent', models.DecimalField(max_digits=14, decimal_places=2, default=0)),
                ('start_date', models.DateField(null=True, blank=True)),
                ('end_date', models.DateField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='MarketingContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.CASCADE, related_name='marketing_content')),
                ('campaign', models.ForeignKey('marketing.campaign', null=True, blank=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contents')),
                ('title', models.CharField(max_length=255)),
                ('body', models.TextField(blank=True)),
                ('content_type', models.CharField(max_length=20, choices=[('post', 'Post'), ('article', 'Article'), ('email', 'Email'), ('video', 'Video'), ('landing_page', 'Landing page'), ('other', 'Other')], default='post')),
                ('status', models.CharField(max_length=20, choices=[('draft', 'Draft'), ('scheduled', 'Scheduled'), ('published', 'Published')], default='draft')),
                ('publish_at', models.DateTimeField(null=True, blank=True)),
                ('published_at', models.DateTimeField(null=True, blank=True)),
                ('url', models.URLField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={'ordering': ['-updated_at']},
        ),
        migrations.CreateModel(
            name='LeadSource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.CASCADE, related_name='marketing_lead_sources')),
                ('name', models.CharField(max_length=160)),
                ('channel', models.ForeignKey('marketing.marketingchannel', null=True, blank=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lead_sources')),
                ('campaign', models.ForeignKey('marketing.campaign', null=True, blank=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lead_sources')),
                ('description', models.TextField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('contacts', models.ManyToManyField('crm.contact', blank=True, related_name='lead_sources')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['name']},
        ),
    ]
