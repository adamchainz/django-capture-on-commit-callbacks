from unittest import mock

from django.db import DEFAULT_DB_ALIAS, connections


class capture_commit_hooks:
    def __init__(self, *, using=DEFAULT_DB_ALIAS, execute=False):
        self.using = using
        self.execute = execute
        self.hooks = None

    def __enter__(self):
        if self.hooks is not None:
            raise RuntimeError("Cannot re-enter capture_commit_hooks()")
        self.hooks = []
        connection = connections[self.using]
        orig_on_commit = connection.on_commit

        def on_commit_wrapper(func):
            self.hooks.append(func)
            return orig_on_commit(func)

        self.patcher = mock.patch.object(connection, "on_commit", on_commit_wrapper)
        self.patcher.start()
        return self.hooks

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.patcher.stop()
        if exc_type is None and self.execute:
            for hook in self.hooks:
                hook()


class TestCaseMixin:
    def captureCommitHooks(self, *, using=DEFAULT_DB_ALIAS, execute=False):
        return capture_commit_hooks(using=using, execute=execute)
