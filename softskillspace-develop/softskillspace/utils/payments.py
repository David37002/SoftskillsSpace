import stripe
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.utils.crypto import get_random_string

from payment.models import LessonPayment, LessonPaymentStatus
from softskillspace.utils.choices import LessonStatus, PaymentMethodChoice
from softskillspace.utils.urls import get_url


def lesson_payment_with_stripe(
        request,
        amount,
        token,
        lesson,
        contact_error_msg=""):
    """
    Handles payment of lesson by stripe
    """
    error_occurred = True

    try:
        total_cost = int(amount)
        charge = stripe.Charge.create(
            amount=total_cost * 100,
            currency="ngn",
            source=token,
            statement_descriptor_suffix="soft skill space",
        )

        # create the payment
        payment = LessonPayment()
        payment.transaction_id = charge.id
        payment.receipt_url = charge.receipt_url

        payment.name_on_card = str(lesson.student)
        payment.lesson = lesson
        payment.amount_gross = total_cost
        payment.payment_method = PaymentMethodChoice.Stripe
        payment.amount_paid = total_cost
        payment.amount_fee = total_cost
        payment.amount_net = int(total_cost * 0.85)
        payment.amount_gross = total_cost
        payment.status = LessonPaymentStatus.Paid
        payment.save()

        lesson.status = LessonStatus.Approved
        lesson.save()

        send_confirmation_email(request, lesson)

        messages.success(request, "Your booking was successful!")
        error_occurred = False

    except stripe.error.CardError as e:
        body = e.json_body
        err = body.get("error", {})
        messages.warning(request, f"{err.get('message')}")

    except stripe.error.RateLimitError as e:
        print(e)
        # Too many requests made to the API too quickly
        messages.warning(request, "Please try again shortly")

    except stripe.error.InvalidRequestError as e:
        # Invalid parameters were supplied to Stripe's API
        print(e)
        messages.warning(
            request,
            "Invalid details specified. Please try again")

    except stripe.error.AuthenticationError as e:
        # Authentication with Stripe's API failed
        # (maybe you changed API keys recently)
        print(e)
        _msg = (
            "We are unable to complete your request at the moment. " +
            contact_error_msg)
        messages.warning(request, _msg)

    except stripe.error.APIConnectionError as e:
        # Network communication with Stripe failed
        print(e)
        messages.warning(
            request, f"Error with our payment provider. {contact_error_msg}"
        )

    except stripe.error.StripeError as e:
        # Display a very generic error to the user, and maybe send
        # yourself an email
        print(e)
        messages.warning(
            request,
            "Something went wrong but you were not charged. Please try again.",
        )

    except (ValueError, ZeroDivisionError, AttributeError) as e:
        # send an email to ourselves
        print(e)
        messages.warning(
            request,
            "A serious error occurred. We have been notified.")

    if error_occurred:
        return redirect("lesson:detail", uuid=lesson.uuid)

    return True


def send_confirmation_email(request, lesson):
    """
    Send confirmation email helper
    """
    url = get_url(request, "lesson:detail", args=[lesson.uuid])

    msg_to_student = (
        f"Hi {lesson.student}\n\n"
        + f"This is to acknowledge that a payment of ₦{lesson.total_cost} "
        + f"has just been received for the lesson {lesson.subject} "
        + f"on {lesson.start_date_format}\n\n"
        + f"More information at {url}\n"
        + "Kind Regards\n"
        + "Soft Skill Space team"
    )

    send_mail(
        subject="Soft Skill Space - Payment received",
        message=msg_to_student,
        fail_silently=True,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[lesson.student.email],
    )

    msg_to_tutor = (
        f"Hi {lesson.tutor}\n\n" +
        f"{lesson.student} has paid for the booking of the lesson " +
        f"'{lesson.subject}' due to take place on {lesson.start_date_format}\n\n" +
        "Congratulations, you may now attend the lesson\n" +
        f"More information at {url}\n" +
        "Kind Regards\n" +
        "Soft Skill Space team")

    send_mail(
        subject="Soft Skill Space - Booking approved",
        message=msg_to_tutor,
        fail_silently=True,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[lesson.tutor.user.email],
    )


def make_free_payment(request, lesson):
    """
    Allows setting values for free payment
    """
    total_cost = 0
    # create the payment
    payment = LessonPayment()
    payment.transaction_id = f"free_{get_random_string(12)}"
    payment.receipt_url = get_url(request, "lesson:detail", args=[lesson.uuid])

    payment.name_on_card = str(lesson.student)
    payment.lesson = lesson
    payment.amount_gross = total_cost
    payment.payment_method = PaymentMethodChoice.SoftPoint
    payment.amount_paid = total_cost
    payment.amount_fee = total_cost
    payment.amount_net = total_cost
    payment.amount_gross = total_cost
    payment.status = LessonPaymentStatus.Paid
    payment.save()

    lesson.status = LessonStatus.Approved
    lesson.save()

    send_confirmation_email(request, lesson)

    messages.success(request, "Your booking was successful!")
    return redirect("lesson:detail", uuid=lesson.uuid)
