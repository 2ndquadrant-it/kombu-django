# Celery Django-based backend

This application starts from the work that have been dismissed from the Kombu
project (from [this commit](https://github.com/celery/kombu/commit/65f982ccf31b86157c39a8feb42081410b83abe2 )), and keeps it updated for the new releases of Django.

To use this backend, you need to list `kombu_django` from your list of installed apps:

```
INSTALLED_APPS = [
    ...
    'kombu_django',
    ...
]
```

and then choose the `django` broker backend:

```
CELERY_BROKER_URL = 'django://'
```

## Using the database as a task result storage

Since you are already using a database as a broker, you can also use it to
store the results of the tasks. To do this, you must list
`django_celery_results` in the installed applications:

```
INSTALLED_APPS = [
    ...
    'django_celery_results',
    ...
]
```

and then activate the new result backend:

```
CELERY_RESULT_BACKEND = 'django-db'
```


## Migrations

Remember to execute the migrations to create the missing tables for the broker
and for the tasks result:

```
$ ./manage.py migrate
[...]
```