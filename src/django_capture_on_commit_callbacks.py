from django.db import DEFAULT_DB_ALIAS, connections


class capture_on_commit_callbacks:
    def __init__(self, *, using=DEFAULT_DB_ALIAS, execute=False):
        self.using = using
        self.execute = execute
        self.callbacks = None

    def __enter__(self):
        if self.callbacks is not None:
            raise RuntimeError("Cannot re-enter capture_on_commit_callbacks()")
        self.start_count = len(connections[self.using].run_on_commit)
        self.callbacks = []
        return self.callbacks

    def __exit__(self, exc_type, exc_val, exc_tb):
        run_on_commit = connections[self.using].run_on_commit[self.start_count :]
        self.callbacks[:] = [func for sids, func in run_on_commit]
        if exc_type is None and self.execute:
            for hook in self.callbacks:
                hook()


class TestCaseMixin:
    @classmethod
    def captureOnCommitCallbacks(cls, *, using=DEFAULT_DB_ALIAS, execute=False):
        return capture_on_commit_callbacks(using=using, execute=execute)
