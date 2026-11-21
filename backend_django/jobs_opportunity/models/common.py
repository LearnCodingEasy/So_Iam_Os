from django.core.validators import MaxValueValidator, MinValueValidator


PERCENT = [MinValueValidator(0), MaxValueValidator(100)]
