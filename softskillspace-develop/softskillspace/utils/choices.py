from django.db import models


class Gender(models.TextChoices):
    Male = ("male", "Male")
    Female = ("female", "Female")
    Other = ("other", "Other")


class AccountType(models.TextChoices):
    Tutor = ("tutor", "Tutor")
    Instructor = ("instructor", "Instructor")


class AcademicLevel(models.TextChoices):
    CollegeCert = ("college_cert", "College Cert")
    Certificate = ("certificate", "Certificate")
    Diploma = ("diploma", "Diploma")
    Degree = ("degree", "Degree")
    Masters = ("masters", "Masters")
    PhD = ("phd", "PhD")


class InstitutionType(models.TextChoices):
    NurserySchool = ("nursery school", "Nursery School")
    PrimarySchool = ("primary school", "Primary School")
    HighSchool = ("high school", "High School")
    College = ("college", "College")
    University = ("university", "University")
    Online = ("online", "Online")
    Other = ("other", "Other")


class LessonPaymentStatus(models.TextChoices):
    Pending = ("pending", "Pending")
    Paid = ("paid", "Paid")


class LessonStatus(models.TextChoices):
    Pending = ("pending", "Pending")
    Approved = ("approved", "Approved")
    Cancelled = ("cancelled", "Cancelled")


class LessonDuration(models.TextChoices):
    MIN_30 = (30, "0h 30m")
    MIN_60 = (60, "1h 00m")
    MIN_90 = (90, "1h 30m")
    MIN_120 = (120, "2h 00m")
    MIN_150 = (150, "2h 30m")
    MIN_180 = (180, "3h 00m")
    MIN_210 = (210, "3h 30m")


class PaymentMethodChoice(models.TextChoices):
    Stripe = ("stripe", "Stripe")
    FlutterWave = ("flutterwave", "Flutterwave")
    SoftPoint = ("point", "Soft Point")


class BootstrapBackground(models.TextChoices):
    Danger = ("bg-danger", "Danger")
    Dark = ("bg-dark", "Dark")
    Dribble = ("bg-dribbble", "Dribbble")
    Facebook = ("bg-facebook", "Facebook")
    Google = ("bg-google", "Google")
    Info = ("bg-info", "Info")
    Instagram = ("bg-instagram", "Instagram")
    Light = ("bg-light", "Light")
    LinkedIn = ("bg-linkedin", "LinkedIn")
    Orange = ("bg-orange", "Orange")
    Pinterest = ("bg-pinterest", "Pinterest")
    Primary = ("bg-primary", "Primary")
    Purple = ("bg-purple", "Purple")
    Secondary = ("bg-secondary", "Secondary")
    Skype = ("bg-skype", "Skype")
    Success = ("bg-success", "Success")
    Transparent = ("bg-transparent", "Transparent")
    Twitter = ("bg-twitter", "Twitter")
    Warning = ("bg-warning", "Warning")
    White = ("bg-white", "White")
    YouTube = ("bg-youtube", "YouTube")


class MailingListType(models.TextChoices):
    ComingSoon = ("coming_soon", "Coming soon")
    NewsLetter = ("newsletter", "Newsletter")
