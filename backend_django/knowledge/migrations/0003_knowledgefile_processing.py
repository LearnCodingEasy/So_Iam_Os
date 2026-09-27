from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [("knowledge", "0002_rename_knowledge_k_knowled_c6a337_idx_knowledge_file_type_idx_and_more")]
    operations = [
        migrations.AddField(model_name="knowledgefile", name="processing_status", field=models.CharField(choices=[("pending","Pending"),("processing","Processing"),("completed","Completed"),("failed","Failed")], default="pending", max_length=20)),
        migrations.AddField(model_name="knowledgefile", name="processed_at", field=models.DateTimeField(blank=True, null=True)),
        migrations.AddField(model_name="knowledgefile", name="processing_error", field=models.TextField(blank=True)),
    ]
