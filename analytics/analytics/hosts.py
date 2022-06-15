from django.conf import settings
from django_hosts import patterns, host

host_patterns = patterns('',
    host(r'accounts', 'apps.accounts.urls', name='accounts'),
    host(r'analysis', 'apps.analysis.urls', name='analysis'),
    host(r'commerce.shop', 'apps.shop.urls', name='shop'),
    host(r'commerce.cart', 'apps.cart.urls', name='cart'),
    host(r'commerce.order', 'apps.order.urls', name='order'),
    host(r'(|www)', settings.ROOT_URLCONF, name='www'),
)
