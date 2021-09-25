from django.core import mail
from django.db import transaction
from django.db.utils import IntegrityError
from django.test import TestCase

from django_capture_on_commit_callbacks import (
    TestCaseMixin,
    capture_on_commit_callbacks,
)


class CaptureOnCommitCallbacksTests(TestCase):
    databases = ["default", "other"]

    def test_with_no_arguments(self):
        with capture_on_commit_callbacks() as callbacks:
            response = self.client.post(
                "/contact/",
                {"message": "I like your site"},
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(callbacks), 1)
        # Execute the hook
        callbacks[0]()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Contact Form")
        self.assertEqual(mail.outbox[0].body, "I like your site")

    def test_with_execute(self):
        with capture_on_commit_callbacks(execute=True) as callbacks:
            response = self.client.post(
                "/contact/",
                {"message": "I like your site"},
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(callbacks), 1)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Contact Form")
        self.assertEqual(mail.outbox[0].body, "I like your site")

    def test_with_alternate_database(self):
        with capture_on_commit_callbacks(using="other", execute=True) as callbacks:
            response = self.client.post(
                "/contact/",
                {"message": "I like your site", "using": "other"},
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(callbacks), 1)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Contact Form")
        self.assertEqual(mail.outbox[0].body, "I like your site")

    def test_wih_rolled_back_savepoint(self):
        with capture_on_commit_callbacks() as callbacks:
            try:
                with transaction.atomic():
                    self.client.post(
                        "/contact/",
                        {"message": "I like your site"},
                    )
                    raise IntegrityError()
            except IntegrityError:
                # inner transaction.atomic() has been rolled back.
                pass

        self.assertEqual(callbacks, [])

    def test_execute_recursive(self):
        callback_called = False

        def enqueue_callback():
            def hook():
                nonlocal callback_called
                callback_called = True

            transaction.on_commit(hook)

        with capture_on_commit_callbacks(execute=True) as callbacks:
            transaction.on_commit(enqueue_callback)

        self.assertEqual(len(callbacks), 2)
        self.assertTrue(callback_called)


class TestCaseMixinTests(TestCaseMixin, TestCase):
    databases = ["default", "other"]

    def test_with_execute(self):
        with self.captureOnCommitCallbacks(execute=True) as callbacks:
            response = self.client.post(
                "/contact/",
                {"message": "I like your site"},
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(callbacks), 1)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Contact Form")
        self.assertEqual(mail.outbox[0].body, "I like your site")
