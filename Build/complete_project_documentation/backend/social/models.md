# social models

Model files and declarations are extracted from source. Field excerpts retain source line numbers; inspect linked source for multiline options and complete semantics.


## common
Source: social/models/common.py

## follow
Source: social/models/follow.py

- L6: class Follow(models.Model):

- L8: id = models.UUIDField(

- L26: created_at = models.DateTimeField(

- L30: class Meta:

- L31: constraints = [

- L32: models.UniqueConstraint(

## friendship
Source: social/models/friendship.py

- L6: class Friendship(models.Model):

- L8: id = models.UUIDField(

- L26: created_at = models.DateTimeField(

- L30: class Meta:

- L33: constraints = [

- L34: models.UniqueConstraint(

## friendship_request
Source: social/models/friendship_request.py

- L6: class FriendshipRequest(models.Model):

- L8: class Status(models.TextChoices):

- L14: id = models.UUIDField(

- L32: status = models.CharField(

- L38: created_at = models.DateTimeField(

- L42: updated_at = models.DateTimeField(

- L46: class Meta:

- L49: constraints = [

- L50: models.UniqueConstraint(

## social_profile
Source: social/models/social_profile.py

- L5: class SocialProfile(models.Model):

- L6: user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="social_profile")

- L7: learning_interests = models.JSONField(default=list, blank=True)

- L8: professional_interests = models.JSONField(default=list, blank=True)

- L9: topics = models.JSONField(default=list, blank=True)

- L10: looking_for = models.JSONField(default=list, blank=True)

- L11: bio = models.TextField(blank=True)

- L12: discoverable = models.BooleanField(default=True)

- L13: updated_at = models.DateTimeField(auto_now=True)

- L15: class Meta:

- L16: indexes = [models.Index(fields=["discoverable", "updated_at"])]

## social_recommendation
Source: social/models/social_recommendation.py

- L5: class SocialRecommendation(models.Model):

- L8: score = models.PositiveSmallIntegerField(default=0)

- L9: reasons = models.JSONField(default=list, blank=True)

- L10: breakdown = models.JSONField(default=dict, blank=True)

- L11: status = models.CharField(max_length=20, default="active")

- L12: created_at = models.DateTimeField(auto_now_add=True)

- L13: updated_at = models.DateTimeField(auto_now=True)

- L15: class Meta:

- L16: constraints = [models.UniqueConstraint(fields=["user", "candidate"], name="unique_social_recommendation")]

- L17: indexes = [models.Index(fields=["user", "score"])]

## user_block
Source: social/models/user_block.py

- L6: class UserBlock(models.Model):

- L8: id = models.UUIDField(

- L26: created_at = models.DateTimeField(

- L30: class Meta:

- L31: constraints = [

- L32: models.UniqueConstraint(

## __init__
Source: social/models/__init__.py


Cross-app references and ownership must be confirmed from fields and write paths. See [project data catalog](../../06-database-and-model-catalog.md).
