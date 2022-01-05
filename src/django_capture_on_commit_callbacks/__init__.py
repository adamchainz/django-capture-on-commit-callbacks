from contextlib import contextmanager
from typing import Any, Callable, ContextManager, Generator, List

import django
from django.core.exceptions import ImproperlyConfigured
from django.db import DEFAULT_DB_ALIAS, connections


def check_django_version() -> None:
    if django.VERSION >= (4, 0):
        raise ImproperlyConfigured(
            "django-capture-on-commit-callbacks is unnecessary on Django "
            + "4.0+. The functionality has been merged as "
            + "TestCase.captureOnCommitCallbacks()"
        )


@contextmanager
def capture_on_commit_callbacks(
    *, using: str = DEFAULT_DB_ALIAS, execute: bool = False
) -> Generator[List[Callable[[], None]], None, None]:
    check_django_version()

    callbacks: List[Callable[[], None]] = []
    start_count = len(connections[using].run_on_commit)
    try:
        yield callbacks
    finally:
        while True:
            callback_count = len(connections[using].run_on_commit)
            for _, callback in connections[using].run_on_commit[start_count:]:
                callbacks.append(callback)
                if execute:
                    callback()

            if callback_count == len(connections[using].run_on_commit):
                break
            start_count = callback_count


class TestCaseMixin:
    @classmethod
    def __init_subclass__(cls, *args: Any, **kwargs: Any) -> None:
        check_django_version()
        super().__init_subclass__(*args, **kwargs)

    @classmethod
    def captureOnCommitCallbacks(
        cls, *, using: str = DEFAULT_DB_ALIAS, execute: bool = False
    ) -> ContextManager[List[Callable[[], None]]]:
        return capture_on_commit_callbacks(using=using, execute=execute)
