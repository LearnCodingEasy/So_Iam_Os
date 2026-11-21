# users_accounts models

Model files and declarations are extracted from source. Field excerpts retain source line numbers; inspect linked source for multiline options and complete semantics.


## custom_user_manager
Source: users_accounts/models/custom_user_manager.py

- L4: class CustomUserManager(UserManager):

## user
Source: users_accounts/models/user.py

- L8: class User(AbstractBaseUser, PermissionsMixin):

- L10: id = models.UUIDField(

- L17: name = models.CharField(

- L21: surname = models.CharField(

- L26: email = models.EmailField(

- L31: date_of_birth = models.DateField(

- L42: gender = models.CharField(

- L48: avatar = models.ImageField(

- L54: cover = models.ImageField(

- L60: skills = models.JSONField(

- L66: is_active = models.BooleanField(

- L70: is_staff = models.BooleanField(

- L74: is_online = models.BooleanField(

- L79: task_count = models.PositiveIntegerField(

- L83: date_joined = models.DateTimeField(

## __init__
Source: users_accounts/models/__init__.py


Cross-app references and ownership must be confirmed from fields and write paths. See [project data catalog](../../06-database-and-model-catalog.md).
