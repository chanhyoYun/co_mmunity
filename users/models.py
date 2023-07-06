from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class MyUserManager(BaseUserManager):
    def create_user(self, email,  password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    """유저 모델
    
    Attributes:
        email (EmailField) : 로그인 이메일
        profile_image (CharField) : DALL-E(AI)를 통한 프로필 이미지 생성 키워드
        profile_image_url (URLField) : DALL-E(AI)를 통한 프로필 이미지 URL
        profile_image_image (ImageField) : 프로필 이미지 생성이 아닌 프로필 이미지 직접 업로드
        followings (ManyToManyField) : 유저 팔로잉
        is_active (BooleanField) : 활성화 여부
        is_admin (BooleanField) : 관리자 여부
    
    """
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    
    profile_image = models.CharField(blank=True, max_length=500)
    profile_image_url = models.URLField(blank=True, max_length=500)
    profile_image_image = models.ImageField(blank=True)
    
    followings = models.ManyToManyField("self", symmetrical=False, related_name='followers', blank=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property  
    def is_staff(self):
        return self.is_admin

