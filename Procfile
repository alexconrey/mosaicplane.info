release: cd src/api && python manage.py migrate && python manage.py seed_exact && python manage.py collectstatic --noinput
web: cd src/api && gunicorn mosaicplane.wsgi:application --bind 0.0.0.0:$PORT