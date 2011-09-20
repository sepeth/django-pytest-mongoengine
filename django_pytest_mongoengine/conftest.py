import os, sys
sys.path.append('.')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from django.conf import settings
from django.test.client import Client
from django.test.utils import setup_test_environment, teardown_test_environment
from django.core.management import call_command
from django.core import mail

from mongoengine.django.auth import User

def create_test_db():
    import mongoengine
    mongoengine.connect(settings.TEST_DB)

def drop_test_db():
    import pymongo
    conn = pymongo.Connection()
    conn.drop_database(settings.TEST_DB)

def pytest_funcarg__django_client(request):
    '''py.test funcargs are awesome. This ugly function basically creates a
    test environment with an empty database every time you write a test
    function that accepts an argument named 'django_client.' Most of the time
    you won't use this, you'll use the 'client' funcarg below instead. This
    funcarg is only reset once per test session. The 'client' funcarg empties
    the database after each test to ensure a clean slate.'''
    def setup():
        setup_test_environment()
        if not hasattr(settings, 'DEBUG'):
            settings.DEBUG = False
        create_test_db()
        return Client()
    def teardown(client):
        drop_test_db()
        teardown_test_environment()
    return request.cached_setup(setup, teardown, "session")

def pytest_funcarg__client(request):
    '''Creates a test environment using the 'django_client' funcarg above, but
    also ensures the database is flushed after running each test.'''
    def setup():
        return request.getfuncargvalue('django_client')
    def teardown(client):
        drop_test_db()
        mail.outbox = []
    return request.cached_setup(setup, teardown, "function")

# Note: I make test usernames and passwords identical for easy login
def pytest_funcarg__user(request):
    '''Create a user with no special permissions.'''
    user = User.create_user(username="user", password="user", email="user@example.com")
    return user

def pytest_funcarg__admin(request):
    '''Create an admin user with all permissions.'''
    admin = User.create_user(username="admin", password="admin", email="admin@example.com")
    admin.is_superuser = True
    admin.save()
    return admin
