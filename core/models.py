from abc import ABC, abstractmethod
from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager

from django.utils import timezone


class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("You have not provided a valid e-mail address")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(blank=True, default="", unique=True)
    name = models.CharField(max_length=255, blank=True, default="")
    password = models.CharField(max_length=255, blank=True, default="1234")

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name or self.email.split("@")[0]

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title + "\n" + self.description

class AcademicQualification(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Address(models.Model, ABC):
    """
    Abstract Django model that provides common address fields and enforces
    the implementation of a validation method in its concrete subclasses.
    """

    local_address = models.CharField(max_length=200)
    division = models.CharField(max_length=200)
    district = models.CharField(max_length=200)
    upazilla = models.CharField(max_length=200)
    post_office = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=200)

    class Meta:
        abstract = True

    @abstractmethod
    def is_valid(self) -> bool:
        pass

    def __str__(self):
        return f"{self.local_address}, {self.district}"

class PermanentAddress(Address):
    years_at_residence = models.IntegerField(default=0)

    def is_valid(self) -> bool:
        """
        Implementation of the abstract method:
        A Permanent Address is valid if residency is at least 1 year.
        """
        pass

    class Meta:
        verbose_name = "Permanent Address"
        verbose_name_plural = "Permanent Addresses"

class PresentAddress(Address):

    def is_valid(self) -> bool:
        """
        Implementation of the abstract method:
        A Present Address is valid if the postal code is exactly 5 digits.
        """
        # Checks if the postal code is 5 digits long.
        return len(self.postal_code) == 5 and self.postal_code.isdigit()

    class Meta:
        verbose_name = "Present Address"
        verbose_name_plural = "Present Addresses"

class PersonalInformation(models.Model):
    name = models.CharField(max_length=200)
    nid_number = models.CharField(max_length=200)
    blood_group = models.CharField(max_length=200) # choice field
    marital_status = models.CharField(max_length=200) # choice field
    religion = models.CharField(max_length=200) # choice field
    sex = models.CharField(max_length=200) # choice field
    email_address = models.CharField(max_length=200, blank=True)
    phone_number = models.CharField(max_length=200, blank=True)
    present_address = models.ForeignKey(PresentAddress, on_delete=models.CASCADE)
    permanent_address = models.ForeignKey(PermanentAddress, on_delete=models.CASCADE)
    date_of_birth = models.CharField(max_length=200)
    academic_qualification = models.ForeignKey(AcademicQualification, on_delete=models.CASCADE)
    upload_certificate = models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class BoeslInformation(models.Model):
    password = models.CharField(max_length=200)
    otp = models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class OldPassportInformation(models.Model):
    passport_no = models.CharField(max_length=200)
    issue_date = models.DateField()
    expiry_date = models.DateField()
    place_of_issue = models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class PassportInformation(models.Model):
    passport_no = models.CharField(max_length=200)
    issue_date = models.DateField()
    expiry_date = models.DateField()
    place_of_issue = models.CharField(max_length=200)
    old_passports_information = models.ForeignKey(OldPassportInformation, on_delete=models.CASCADE)
    name_of_emergency_contact_person = models.CharField(max_length=200)
    relation = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class PreviousExperience(models.Model):
    company_name = models.CharField(max_length=200)
    from_year = models.DateField()
    to_year = models.DateField()
    year_of_work = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class WorkInformation(models.Model):
    current_occupation = models.CharField(max_length=200, default="None")
    total_years_of_experience = models.IntegerField(default=0, blank=True, null=True)
    technical_qualification = models.CharField(max_length=200, default="None")
    company_name = models.CharField(max_length=200, default="None")
    from_year = models.DateField(blank=True, null=True)
    to_year = models.DateField(blank=True, null=True)
    year_of_work = models.IntegerField(default=0)
    place_of_work = models.CharField(max_length=200)
    earning_salary = models.IntegerField(default=0)
    previous_experiences = models.ManyToManyField(PreviousExperience, blank=True, null=True, default=None)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class FamilyDetails(models.Model):
    fathers_name = models.CharField(max_length=200)
    fathers_contact_number = models.CharField(max_length=200)
    mothers_name = models.CharField(max_length=200)
    mothers_contact_number = models.CharField(max_length=200)
    third_family_member_name = models.CharField(max_length=200)
    third_family_member_relation_with = models.CharField(max_length=200)
    third_family_member_contact_number = models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.fathers_name
    
class CandidateInformation(models.Model):
    personal_information = models.ForeignKey(PersonalInformation, on_delete=models.CASCADE, blank=True, null=True)
    boesl_information = models.ForeignKey(BoeslInformation, on_delete=models.CASCADE, blank=True, null=True)
    passport_information = models.ForeignKey(PassportInformation, on_delete=models.CASCADE, blank=True, null=True)
    work_information = models.ForeignKey(WorkInformation, on_delete=models.CASCADE, blank=True, null=True)
    family_details = models.ForeignKey(FamilyDetails, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name