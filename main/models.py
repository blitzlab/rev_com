import random
from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# User Manager

class MyUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        """
        Creates and saves a User with the given information.
        """
        if not email:
            raise ValueError('Users must have an email address')
        if not first_name:
            raise ValueError('Users must have first name')
        if not last_name:
            raise ValueError('Users must have last name')
        # if not username:
        #     raise ValueError('Users must have a username')
        # if not phone_number:
        #     raise ValueError('Users must have an email address valid phone number')
        # if not gender:
        #     raise ValueError('Users must specify gender')
        # if not country:
        #     raise ValueError('Users must have a country')

        user = self.model(
            email=self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            # username = username,
            # phone_number = phone_number,
            # gender = gender,
            # country = country,
            ref_id = str(random.randrange(1000, 9999, 4))
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    # def create_superuser(self, email, first_name, last_name, username, phone_number, gender, country, password=None):
    def create_superuser(self, email, first_name, last_name, password=None):
        """
        Creates and saves a superuser with the given information.
        """
        user = self.create_user(
            email=self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            # username = username,
            # phone_number = phone_number,
            # gender = gender,
            # country = country,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

# Create your models here.
class User(AbstractBaseUser):

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Others')
    )

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    username = models.CharField(unique=True, max_length=50, null=True, blank=True)
    email = models.EmailField(unique=True, max_length=254)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    phone_number = models.CharField(null=True, blank=True, unique=True, max_length=15)
    country = models.CharField(max_length = 20, null=True, blank=True)
    referrer = models.CharField(max_length = 20, null=True, blank=True)
    ref_id = models.CharField(unique = True, max_length = 20, null=True, blank=True)
    email_confirmed = models.BooleanField(default = False)
    registered_on = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default = False)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)
    is_superuser = models.BooleanField(default = False)

    REQUIRED_FIELDS = ['first_name', 'last_name']
    USERNAME_FIELD = 'email'

    object = MyUserManager()

    def __str__(self):
        return self.first_name+" "+self.last_name

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def get_absolute_url(self):
        return reverse("main:profile", kwargs={'pk': self.pk})

class UserLogins(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "User Logins"

    def __str__(self):
        return str(self.user)

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=19, decimal_places=2, null = True)


    def __str__(self):
        return self.user.first_name+" "+self.user.last_name

    class Meta:
        verbose_name_plural = "User Wallets"
        constraints = [
        models.UniqueConstraint(fields=['user', 'balance'], name='user_wallet')
        ]


class Upgrade(models.Model):
    name = models.CharField(max_length = 50, null = True, blank = True)
    price = models.DecimalField(max_digits=19, decimal_places=2, null = True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Upgrade"
        constraints = [
        models.UniqueConstraint(fields=['name', 'price'], name='premium_package')
        ]


class WithdrawRequest(models.Model):
    STATUS_CHOICES = [
        ('Approved', 'Approved'),
        ('Declined', 'Declined'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null = True)
    bank_name = models.CharField(max_length = 50, null = True, blank = True)
    account_number = models.CharField(max_length = 50, null = True, blank = True)
    status = models.CharField(max_length=10, default="Pending", choices=STATUS_CHOICES)
    request_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Withdraw Requests"

    def __str__(self):
        return self.user.first_name +" "+ self.user.last_name


class PremiumUser(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    upgrade_on = models.DateTimeField(auto_now = True)

    class Meta:
        verbose_name_plural = "Premium Users"

    def __str__(self):
        return self.user.first_name +" "+ self.user.last_name

class SignupBonus(models.Model):
    amount = models.DecimalField(max_digits=19, decimal_places=2, null = True)

    class Meta:
        verbose_name_plural = "Signup Bonus"

    def __str__(self):
        return str(self.amount)

class LoginBonus(models.Model):
    amount = models.DecimalField(max_digits=19, decimal_places=2, null = True)

    class Meta:
        verbose_name_plural = "Login Bonus"

    def __str__(self):
        return str(self.amount)

class PremiumLoginBonus(models.Model):
    amount = models.DecimalField(max_digits=19, decimal_places=2, null = True)

    class Meta:
        verbose_name_plural = "Premium User Login Bonus"

    def __str__(self):
        return str(self.amount)

class ReferBonus(models.Model):
    amount = models.DecimalField(max_digits=19, decimal_places=2, null = True)

    class Meta:
        verbose_name_plural = "Refer Bonus"

    def __str__(self):
        return str(self.amount)

class PremiumReferBonus(models.Model):
    amount = models.DecimalField(max_digits=19, decimal_places=2, null = True)

    class Meta:
        verbose_name_plural = "Premium User Refer Bonus"

    def __str__(self):
        return str(self.amount)

class PremiumUserReferUpgradeBonus(models.Model):
    amount = models.DecimalField(max_digits=19, decimal_places=2, null = True)

    class Meta:
        verbose_name_plural = "Premium User Refer Upgrade Bonus"

    def __str__(self):
        return str(self.amount)

class AllEarnings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(blank=True, null = True, max_digits=19, decimal_places=2)
    date_earned = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

class CommentBonus(models.Model):
    amount = models.DecimalField(blank=True, null = True, max_digits=19, decimal_places=2)

    class Meta:
        verbose_name_plural = "Comment Bonus"

    def __str__(self):
        return str(self.amount)

class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length = 200, unique=True, null = True, blank = True)
    text = RichTextField(null = True, unique=True, blank = True)
    slug = models.SlugField(max_length=100, null = True, blank = True)
    status = models.CharField(max_length = 200, default="Not Published")
    featured_image = models.ImageField(upload_to="blog/uploads", height_field=None, width_field=None, max_length=100, null = True, blank = True)
    published_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Blogs"


    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        return super(Blog, self).save(*args, **kwargs)


class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(null = True, unique=True, blank = True)
    commented_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "Comments"

class BlogLike(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.BooleanField(default = False)
    liked_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name+" "+self.user.last_name

    class Meta:
        verbose_name_plural = "Blog Likes"


class BlogLikeBonus(models.Model):
    amount = models.DecimalField(blank=True, null = True, max_digits=19, decimal_places=2)

    class Meta:
        verbose_name_plural = "Blog Like Bonus"

    def __str__(self):
        return str(self.amount)

class PremiumBlogLikeBonus(models.Model):
    amount = models.DecimalField(blank=True, null = True, max_digits=19, decimal_places=2)

    class Meta:
        verbose_name_plural = "Premium Blog Like Bonus"

    def __str__(self):
        return str(self.amount)

class PremiumUserCommentBonus(models.Model):
    amount = models.DecimalField(blank=True, null = True, max_digits=19, decimal_places=2)

    class Meta:
        verbose_name_plural = "Premium User Comment Bonus"

    def __str__(self):
        return str(self.amount)

class MinimumWithdrawAmount(models.Model):
    amount = models.DecimalField(blank=True, null = True, max_digits=19, decimal_places=2)

    class Meta:
        verbose_name_plural = "Minimum Withdraw Amount"

    def __str__(self):
        return str(self.amount)
