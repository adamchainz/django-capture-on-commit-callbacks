import django
from django.core import mail
from django.test import TestCase

from django_capture_on_commit_callbacks import (
    TestCaseMixin,
    capture_on_commit_callbacks,
)


class CaptureOnCommitCallbacksTests(TestCase):
    if django.VERSION >= (2, 2):
        databases = ["default", "other"]
    else:
        multi_db = True

    def test_with_no_arguments(self):
        with capture_on_commit_callbacks() as callbacks:
            response = self.client.post("/contact/", {"message": "I like your site"},)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(callbacks), 1)
        # Execute the hook
        callbacks[0]()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Contact Form")
        self.assertEqual(mail.outbox[0].body, "I like your site")

    def test_with_execute(self):
        with capture_on_commit_callbacks(execute=True) as callbacks:
            response = self.client.post("/contact/", {"message": "I like your site"},)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(callbacks), 1)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Contact Form")
        self.assertEqual(mail.outbox[0].body, "I like your site")

    def test_with_alternate_database(self):
        with capture_on_commit_callbacks(using="other", execute=True) as callbacks:
            response = self.client.post(
                "/contact/", {"message": "I like your site", "using": "other"},
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(callbacks), 1)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Contact Form")
        self.assertEqual(mail.outbox[0].body, "I like your site")


class TestCaseMixinTests(TestCaseMixin, TestCase):
    if django.VERSION >= (2, 2):
        databases = ["default", "other"]
    else:
        multi_db = True

    def test_with_execute(self):
        with self.captureOnCommitCallbacks(execute=True) as callbacks:
            response = self.client.post("/contact/", {"message": "I like your site"},)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(callbacks), 1)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Contact Form")
        self.assertEqual(mail.outbox[0].body, "I like your site")
