import os
from django.conf import settings

# Storage on S3 settings are stored as os.environs to keep settings.py clean
if not settings.DEBUG:
    AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
    AWS_PRELOAD_METADATA = True # necessary to fix manage.py collectstatic command to only upload changed files instead of all files
    DEFAULT_FILE_STORAGE = 'speaknow.settings.s3utils.MediaRootS3BotoStorage'
    STATICFILES_STORAGE = 'speaknow.settings.s3utils.StaticRootS3BotoStorage'
    S3_URL = 'http://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME


    # MEDIA_ROOT and STATIC_ROOT are superceded by DEFAULT_FILE_STORAGE and STATICFILES_STORAGE respectively
    # and hence not needed.

    STATIC_URL = S3_URL + 'static/'
    MEDIA_URL = S3_URL + 'media/'



