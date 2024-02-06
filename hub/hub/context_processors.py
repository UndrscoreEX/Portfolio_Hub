
from django.conf import settings

def cloudfront_prefix(request):
    return {'Cloudfront_prefix': settings.CLOUDFRONT_PREFIX}
