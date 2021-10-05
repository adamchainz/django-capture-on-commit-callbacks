=======
History
=======

1.9.0 (2021-10-05)
------------------

* Support Python 3.10.

1.8.0 (2021-09-28)
------------------

* Support Django 4.0.
  Usage raises ``ImproperlyConfigured`` on Django 4.0 since all features are available in Django core.

1.7.0 (2021-09-25)
------------------

* Capture callbacks recursively.
  This backports the new behaviour from Django 4.0 (`Ticket #33054 <https://code.djangoproject.com/ticket/33054>`__).

  Thanks to Eugene Morozov in `PR #118 <https://github.com/adamchainz/django-capture-on-commit-callbacks/pull/118>`__.

* Remove Django 3.2 incompatibility check.
  Because this package now backports the change from Django 4.0, there is a legitimate reason to use this package on Django 3.2.

1.6.0 (2021-08-14)
------------------

* Add type hints.

1.5.0 (2021-06-19)
------------------

* Move incompatibility check for Django 3.2 from a system check to a use time
  check. This is because pytest does not run system checks.

* Stop distributing tests to reduce package size. Tests are not intended to be
  run outside of the tox setup in the repository. Repackagers can use GitHub's
  tarballs per tag.

1.4.0 (2021-01-25)
------------------

* Support Django 3.2.

1.3.0 (2020-12-13)
------------------

* Drop Python 3.5 support.
* Support Python 3.9.

1.2.0 (2020-05-24)
------------------

* Drop Django 2.0 and 2.1 support.
* Use ``@contextlib.contextmanager``.

1.1.0 (2020-05-24)
------------------

* Made ``captureOnCommitCallbacks()`` a ``classmethod`` so it can be used from within class methods such as ``setUpClass()``, ``setUpTestData()``.
* Avoiding capturing callbacks enqueued within rolled back ``atomic()`` blocks.
  As a side effect of this change, the returned list of callbacks is only populated when the context manager exits.
* Add Django 3.1 support.

1.0.0 (2020-05-20)
------------------

* Initial release.
