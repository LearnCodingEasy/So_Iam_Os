# Update AI provider choices to include Gemini and DeepSeek.
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ai", "0002_aiproviderconfig"),
    ]

    operations = [
        migrations.AlterField(
            model_name="aisettings",
            name="preferred_provider",
            field=models.CharField(
                choices=[
                    ("ollama", "Ollama"),
                    ("openai", "OpenAI"),
                    ("openrouter", "OpenRouter"),
                    ("gemini", "Google Gemini"),
                    ("deepseek", "DeepSeek"),
                ],
                default="ollama",
                max_length=50,
            ),
        ),
        migrations.AlterField(
            model_name="aiprovidercredential",
            name="provider",
            field=models.CharField(
                choices=[
                    ("ollama", "Ollama"),
                    ("openai", "OpenAI"),
                    ("openrouter", "OpenRouter"),
                    ("gemini", "Google Gemini"),
                    ("deepseek", "DeepSeek"),
                ],
                max_length=50,
            ),
        ),
        migrations.AlterField(
            model_name="aiconversation",
            name="provider",
            field=models.CharField(
                choices=[
                    ("ollama", "Ollama"),
                    ("openai", "OpenAI"),
                    ("openrouter", "OpenRouter"),
                    ("gemini", "Google Gemini"),
                    ("deepseek", "DeepSeek"),
                ],
                default="ollama",
                max_length=50,
            ),
        ),
    ]
