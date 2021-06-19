from contextlib import contextmanager

import django
from django.core.exceptions import ImproperlyConfigured
from django.db import DEFAULT_DB_ALIAS, connections


def check_django_version():
    if django.VERSION >= (3, 2):
        raise ImproperlyConfigured(
            "django-capture-on-commit-callbacks is unnecessary on Django "
            + "3.2+. The functionality has been merged as "
            + "TestCase.captureOnCommitCallbacks()"
        )


@contextmanager
def capture_on_commit_callbacks(*, using=DEFAULT_DB_ALIAS, execute=False):
    check_django_version()

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
    def __init_subclass__(cls, *args, **kwargs):
        check_django_version()
        super().__init_subclass__(*args, **kwargs)

    @classmethod
    def captureOnCommitCallbacks(cls, *, using=DEFAULT_DB_ALIAS, execute=False):
        return capture_on_commit_callbacks(using=using, execute=execute)
