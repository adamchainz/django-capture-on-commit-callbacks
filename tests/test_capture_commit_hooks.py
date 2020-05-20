import django
from django.core import mail
from django.test import TestCase
from django_capture_commit_hooks import TestCaseMixin, capture_commit_hooks


class CaptureCommitHooksTests(TestCase):
    if django.VERSION >= (2, 2):
        databases = ["default", "other"]
    else:
        multi_db = True

    def test_with_no_arguments(self):
        with capture_commit_hooks() as hooks:
            response = self.client.post("/contact/", {"message": "I like your site"},)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(hooks), 1)
        # Execute the hook
        hooks[0]()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Contact Form")
        self.assertEqual(mail.outbox[0].body, "I like your site")

    def test_with_execute(self):
        with capture_commit_hooks(execute=True) as hooks:
            response = self.client.post("/contact/", {"message": "I like your site"},)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(hooks), 1)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Contact Form")
        self.assertEqual(mail.outbox[0].body, "I like your site")

    def test_with_alternate_database(self):
        with capture_commit_hooks(using="other", execute=True) as hooks:
            response = self.client.post(
                "/contact/", {"message": "I like your site", "using": "other"},
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(hooks), 1)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Contact Form")
        self.assertEqual(mail.outbox[0].body, "I like your site")


class TestCaseMixinTests(TestCaseMixin, TestCase):
    if django.VERSION >= (2, 2):
        databases = ["default", "other"]
    else:
        multi_db = True

    def test_with_execute(self):
        with self.captureCommitHooks(execute=True) as hooks:
            response = self.client.post("/contact/", {"message": "I like your site"},)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(hooks), 1)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Contact Form")
        self.assertEqual(mail.outbox[0].body, "I like your site")
