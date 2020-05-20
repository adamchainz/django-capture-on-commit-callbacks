from django.core import mail
from django.db import DEFAULT_DB_ALIAS, transaction
from django.http import HttpResponse
from django.views.decorators.http import require_POST


@require_POST
def contact(request):
    message = request.POST.get("message", "nothing in particular")
    using = request.POST.get("using", DEFAULT_DB_ALIAS)

    def send_email():
        mail.send_mail(
            subject="Contact Form",
            message=message,
            from_email="from@example.com",
            recipient_list=["to@example.com"],
        )

    transaction.on_commit(send_email, using=using)

    return HttpResponse("Message sent!")
