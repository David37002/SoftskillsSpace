from django.urls import URLPattern, URLResolver, reverse


def list_urls(lis, acc=None):
    """gets all urls so it can be printed from the command line"""
    if acc is None:
        acc = []

    if not lis:
        return

    l = lis[0]

    if isinstance(l, URLPattern):
        yield acc + [str(l.pattern)]

    elif isinstance(l, URLResolver):
        yield from list_urls(l.url_patterns, acc + [str(l.pattern)])

    yield from list_urls(lis[1:], acc)


def get_url(request, path_str, args=()):
    """
    generates full url using the app urls pattern e.g.
    get_url(request, 'admin:index')
    >>> http://localhost:8000/admin/index/

    get_url(request, 'product:detail', [1])
    >>> http://localhost:8000/product/1/
    """
    domain = request.get_host().strip("/")
    scheme = request.scheme
    path = reverse(path_str, args=args).strip("/")
    return f"{scheme}://{domain}/{path}"
