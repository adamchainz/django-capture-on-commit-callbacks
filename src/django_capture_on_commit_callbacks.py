from contextlib import contextmanager

import django
from django.core import checks
from django.db import DEFAULT_DB_ALIAS, connections


@checks.register(checks.Tags.compatibility)
def check_django_version(**kwargs):
    errors = []
    if django.VERSION >= (3, 2):
        errors.append(
            checks.Error(
                id="dcocc.E001",
                msg=(
                    "django-capture-on-commit-callbacks is unnecessary on "
                    + "Django 3.2+."
                ),
                hint=(
                    "The functionality has been merged as "
                    + "TestCase.captureOnCommitCallbacks()"
                ),
            )
        )
    return errors


@contextmanager
def capture_on_commit_callbacks(*, using=DEFAULT_DB_ALIAS, execute=False):
    callbacks = []
    start_count = len(connections[using].run_on_commit)
    try:
        yield callbacks
    finally:
        run_on_commit = connections[using].run_on_commit[start_count:]
        callbacks[:] = [func for sids, func in run_on_commit]
        if execute:
            for callback in callbacks:
                callback()


class TestCaseMixin:
    @classmethod
    def captureOnCommitCallbacks(cls, *, using=DEFAULT_DB_ALIAS, execute=False):
        return capture_on_commit_callbacks(using=using, execute=execute)
