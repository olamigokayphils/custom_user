from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, full_name, password=None, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email=self.normalize_email(email),
            full_name=full_name,
            password=password
        )
        user.staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserSignUp(AbstractBaseUser):
    class Meta:
        verbose_name = "User Sign Up"
        verbose_name_plural = "User Sign Up"
    username = None
    email = models.EmailField(unique=True)
    referral_code = models.CharField(max_length=250, blank=True)
    full_name = models.CharField(max_length=50)
    date_joined = models.DateTimeField(
        verbose_name='date joined', auto_now_add=True
    )
    last_login = models.DateTimeField(
        verbose_name='last login', auto_now=True
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = MyUserManager()

    # This overwrites django's default user model's username to a
    # username of choice
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["full_name"]

    def __str__(self):
        return self.full_name

    def has_perm(self, perm, obj=None):
        """ Does the user have specific perimission?"""
        return self.is_admin

    def has_module_perms(self, app_label):
        """ 
        Does the user have specific permission to view the app'app_label'?
        """
        return True


class RecentTransactions(models.Model):
    class Meta:
        verbose_name = "Recent Transactions"
        verbose_name_plural = "Recent Transactions"
    STATUS_CHOICES = (
        ("Paid", "Paid"),
        ("Unpaid", "Unpaid")
    )
    TRANSACTION_TYPE_CHOICES = (
        ("Deposit", "Deposit"),
        ("Withdrawal", "Withdrawal")
    )
    CURRENCY_CHOICES = (
        ("ETH", "ETH"),
        ("BTC", "BTC")
    )
    DETAIL_CHOICES = (
        ("Deposit to wallet", "Deposit to wallet"),
        ("Withdrawal from wallet", "Withdrawal from wallet")
    )
    
    status = models.CharField(max_length=60, choices=STATUS_CHOICES)
    date = models.DateTimeField(auto_now_add=True)
    merchant = models.CharField(max_length=60)
    transaction_type = models.CharField(
        max_length=60, choices=TRANSACTION_TYPE_CHOICES
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=5, choices=CURRENCY_CHOICES)
    tokens = models.DecimalField(max_digits=9, decimal_places=2)
    details = models.CharField(max_length=100, choices=DETAIL_CHOICES)

    def __str__(self):
        return self.merchant
