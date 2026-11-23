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
        ('projects', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.CASCADE, related_name='sales_offers')),
                ('project', models.ForeignKey('projects.project', null=True, blank=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sales_offers')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('price', models.DecimalField(max_digits=14, decimal_places=2, default=0)),
                ('currency', models.CharField(max_length=3, default='USD')),
                ('status', models.CharField(max_length=20, choices=[('draft', 'Draft'), ('active', 'Active'), ('retired', 'Retired')], default='draft')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={'ordering': ['name']},
        ),
        migrations.CreateModel(
            name='Deal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.CASCADE, related_name='sales_deals')),
                ('contact', models.ForeignKey('crm.contact', null=True, blank=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deals')),
                ('offer', models.ForeignKey('sales.offer', null=True, blank=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deals')),
                ('title', models.CharField(max_length=200)),
                ('value', models.DecimalField(max_digits=14, decimal_places=2, default=0)),
                ('currency', models.CharField(max_length=3, default='USD')),
                ('stage', models.CharField(max_length=20, choices=[('prospecting', 'Prospecting'), ('qualified', 'Qualified'), ('proposal', 'Proposal'), ('negotiation', 'Negotiation'), ('won', 'Won'), ('lost', 'Lost')], default='prospecting')),
                ('expected_close_date', models.DateField(null=True, blank=True)),
                ('closed_at', models.DateTimeField(null=True, blank=True)),
                ('lost_reason', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={'ordering': ['-updated_at']},
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.CASCADE, related_name='sales_records')),
                ('deal', models.ForeignKey('sales.deal', null=True, blank=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sales')),
                ('offer', models.ForeignKey('sales.offer', null=True, blank=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sales')),
                ('contact', models.ForeignKey('crm.contact', null=True, blank=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sales')),
                ('amount', models.DecimalField(max_digits=14, decimal_places=2, default=0)),
                ('currency', models.CharField(max_length=3, default='USD')),
                ('status', models.CharField(max_length=20, choices=[('completed', 'Completed'), ('refunded', 'Refunded')], default='completed')),
                ('sold_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('reference', models.CharField(max_length=120, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['-sold_at']},
        ),
        migrations.CreateModel(
            name='SalesActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.CASCADE, related_name='sales_activities')),
                ('deal', models.ForeignKey('sales.deal', on_delete=django.db.models.deletion.CASCADE, related_name='activities')),
                ('activity_type', models.CharField(max_length=20, choices=[('call', 'Call'), ('email', 'Email'), ('meeting', 'Meeting'), ('demo', 'Demo'), ('proposal', 'Proposal'), ('note', 'Note')], default='note')),
                ('notes', models.TextField(blank=True)),
                ('occurred_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['-occurred_at']},
        ),
    ]
