from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from datetime import datetime, date


class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None, **extra_fields):
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)

        return user


class User(AbstractBaseUser, PermissionsMixin):

    MALE = 'male'
    FEMALE = 'female'
    NA = 'NA'

    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (NA, 'N/A'),
    ]
    STAFF = 'Staff'

    ROLE_CHOICE = [
        (STAFF, 'Staff')
    ]
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(
        max_length=31,
        choices=GENDER_CHOICES,
        default=MALE
    )
    role = models.CharField(
        max_length=31,
        choices=ROLE_CHOICE,
        default=STAFF
    )
    date_of_birth = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    website = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=512, null=True, blank=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    fax = models.CharField(max_length=20, null=True, blank=True)
    telephone = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(default=datetime.now)

    objects = UserManager()

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


class Schedule(models.Model):
    MONDAY = 'monday'
    TUESDAY = 'tuesday'
    WEDNESDAY = 'wednesday'
    THURSDAY = 'thursday'
    FRIDAY = 'friday'
    SATURDAY = 'saturday'
    SUNDAY = 'sunday'

    WEEKDAY_CHOICES = [
        (MONDAY, 'monday'),
        (TUESDAY, 'tuesday'),
        (WEDNESDAY, 'wednesday'),
        (THURSDAY, 'thursday'),
        (FRIDAY, 'friday'),
        (SATURDAY, 'saturday'),
        (SUNDAY, 'sunday'),

    ]
    staff = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='schedules')
    weekDay = models.CharField(
        max_length=31,
        choices=WEEKDAY_CHOICES,
        default=MONDAY
    )

    MORNING = 'morning'
    AFTERNOON = 'afternoon'
    EVENING = 'evening'

    WORKING_TIME_CHOICES = (
        (MORNING, 'morning'),
        (AFTERNOON, 'afternoon'),
        (EVENING, 'evening'),
    )

    workingTime = models.CharField(
        max_length=31,
        choices=WORKING_TIME_CHOICES,
        default=MORNING
    )

    created_at = models.DateTimeField(default=datetime.now)
