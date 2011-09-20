django-pytest-mongoengine
=========================

Forked from https://github.com/buchuki/django-pytest. This fork allows you
to use pytest & mongoengine testrunner with django, instead of
django's default database functionality.

To use it,

- add it to your python path,
- add *django_pytest_mongoengine* to your installed apps.
- set test database name in settings.py (*TEST_DB*)
- set the *TEST_RUNNER = 'django_pytest_mongoengine.test_runner.run_tests'* setting.
- create a conftest.py in your project directory and include:

<pre><code>from django_pytest_mongoengine.conftest import (pytest_funcarg__client,
pytest_funcarg__django_client, pytest_funcarg__user, pytest_funcarg__admin)
</code></pre>

Now anywhere in your project, you can create files called
*test_&lt;something&gt;.py*.  These are standard py.test test files. Use the funcarg
*client* in every test to both instantiate a test database that is cleared
after each test and to provide you with a django test client object identical
to the one used in django's test system. For example:

    def test_filter(client):
        response = client.get('/browse/', {'filter': '1'})
        assert response.status_code == 200

Use *./manage.py test* to run the py.test test runs (ie: it replaces the
standard django test runner). You can pass py.test options to the command
and they will be forwarded to py.test. (Technically, I haven't got it passing
all options, just the most common ones I use)

py.test automatically picks up any subclasses of unittest.TestCase, provided
they are in a module named test_&lt;something&gt;.py. Thus, all your existing django
unittests should work seemlessly with py.test, although you may have to rename
your test files if they do not conform to this convention. You can also write
custom py.test test collection hooks to pick up test modules that are named in
a different directory structure.
