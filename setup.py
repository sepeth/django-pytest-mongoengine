from setuptools import setup
from setuptools import find_packages

setup(
        name="django-pytest-mongoengine",
        version="0.1.4",
        author="Doğan Çeçen",
        author_email="sepeth@gmail.com",
        packages=find_packages(),
        url="http://github.com/sepeth/django-pytest-mongoengine",
        license="LICENSE.txt",
        description="django test runner to use py.test tests",
        long_description=open('README.md').read(),
        zip_safe=False,
)
