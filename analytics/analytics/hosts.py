from django.conf import settings
from django_hosts import patterns, host

host_patterns = patterns('',
    host(r'accounts', 'apps.accounts.urls', name='accounts'),
    host(r'(|www)', settings.ROOT_URLCONF, name='www'),
)
