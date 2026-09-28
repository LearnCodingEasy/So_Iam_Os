from django.db import migrations, models
class Migration(migrations.Migration):
    dependencies = [("learning", "0002_alter_knowledgeapplication_knowledge_item")]
    operations = [migrations.AlterField(model_name="learningnote", name="note_type", field=models.CharField(choices=[("general","General"),("summary","Summary"),("question","Question"),("insight","Insight"),("example","Example"),("confusion","Confusion"),("revision","Revision"),("reflection","Reflection")], default="general", max_length=20))]
