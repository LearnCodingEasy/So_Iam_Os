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
        ('sales', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RevenueSource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.CASCADE, related_name='revenue_sources')),
                ('name', models.CharField(max_length=160)),
                ('source_type', models.CharField(max_length=20, choices=[('service', 'Service'), ('product', 'Product'), ('subscription', 'Subscription'), ('affiliate', 'Affiliate'), ('other', 'Other')], default='service')),
                ('description', models.TextField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['name']},
        ),
        migrations.CreateModel(
            name='RevenueStream',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.CASCADE, related_name='revenue_streams')),
                ('source', models.ForeignKey('revenue.revenuesource', on_delete=django.db.models.deletion.CASCADE, related_name='streams')),
                ('name', models.CharField(max_length=160)),
                ('description', models.TextField(blank=True)),
                ('status', models.CharField(max_length=20, choices=[('active', 'Active'), ('paused', 'Paused'), ('ended', 'Ended')], default='active')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={'ordering': ['name']},
        ),
        migrations.CreateModel(
            name='RevenueRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.CASCADE, related_name='revenue_records')),
                ('stream', models.ForeignKey('revenue.revenuestream', null=True, blank=True, on_delete=django.db.models.deletion.SET_NULL, related_name='records')),
                ('sale', models.ForeignKey('sales.sale', null=True, blank=True, on_delete=django.db.models.deletion.SET_NULL, related_name='revenue_records')),
                ('amount', models.DecimalField(max_digits=14, decimal_places=2, default=0)),
                ('currency', models.CharField(max_length=3, default='USD')),
                ('received_on', models.DateField()),
                ('description', models.CharField(max_length=255, blank=True)),
                ('reference', models.CharField(max_length=120, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['-received_on', '-id'], 'constraints': [models.UniqueConstraint(fields=['sale'], name='revenue_record_sale_unique')]},
        ),
        migrations.CreateModel(
            name='RecurringRevenue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.CASCADE, related_name='recurring_revenue')),
                ('stream', models.ForeignKey('revenue.revenuestream', on_delete=django.db.models.deletion.CASCADE, related_name='recurring_items')),
                ('name', models.CharField(max_length=160, blank=True)),
                ('amount', models.DecimalField(max_digits=14, decimal_places=2, default=0)),
                ('currency', models.CharField(max_length=3, default='USD')),
                ('interval', models.CharField(max_length=20, choices=[('monthly', 'Monthly'), ('quarterly', 'Quarterly'), ('yearly', 'Yearly')], default='monthly')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(null=True, blank=True)),
                ('status', models.CharField(max_length=20, choices=[('active', 'Active'), ('paused', 'Paused'), ('cancelled', 'Cancelled')], default='active')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={'ordering': ['-start_date', '-id']},
        ),
    ]
