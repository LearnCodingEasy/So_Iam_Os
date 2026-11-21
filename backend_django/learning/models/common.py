from django.core.validators import MinValueValidator, MaxValueValidator


SCORE_VALIDATORS = [
    MinValueValidator(0),
    MaxValueValidator(100),
]


MINUTES_VALIDATORS = [MinValueValidator(0)]
