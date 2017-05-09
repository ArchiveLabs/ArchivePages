import web
import internetarchive
from lru import lru_cache_function

urls = (
    '/(.*)', 'hello'
)
app = web.application(urls, globals())

config = dict(general=dict(secure=False))

CUSTOM_DOMAINS = {
    u'experiments.archivelab.org': u'ArchiveExperiments',
    u'archiveexperiments.org': u'ArchiveExperiments',
    u'www.archiveexperiments.org': u'ArchiveExperiments',
    u'pagetest.rchrd.net': u'HelloWebpage',
    u'gifcities.org': 'GifCities',
    u'www.gifcities.org': 'GifCities',
    u'blog.archivelab.org': 'blog-archivelab-org',
}

# Note max_size is number of items, not item size
@lru_cache_function(max_size=1024, expiration=15*60)
def lookup_case_insensitive_identifier(identifier):
    """Perform a case-insensitive lookup"""
    params = dict(page=1)
    search_results = internetarchive.search_items('identifier:' + identifier,
                                                  params=params, config=config)
    ids = [ r['identifier']  for r in search_results ]
    if len(ids) > 0:
        identifier = ids[0]
    return identifier


# Note max_size is number of items, not item size
@lru_cache_function(max_size=1024, expiration=15*60)
def lookup_item_base_url(identifier, default):
    """Does an API request to look up an item
    :return URL to the item (eg "ia600206.us.archive.org/14/items/HelloWebpage")
    """
    item = internetarchive.get_item(identifier, config=config)
    if not item.exists:
        return default

    # Look for an index.html
    if len([ True for f in item.files if f['name'] == 'index.html' ]) == 0:
        return default

    if item.d1:
        return item.d1 + item.dir
    elif item.d2:
        return item.d2 + item.dir
    else:
        return default


class hello:
    def get_identifier_and_item_path(self, web, request_path):
        request_path = request_path.strip('/')
        host = web.ctx.env.get('HTTP_HOST')
        if host in CUSTOM_DOMAINS:
            identifier = CUSTOM_DOMAINS[host]
            item_path = request_path
        else:
            parts = request_path.split('/')
            identifier = parts[0]
            identifier = lookup_case_insensitive_identifier(identifier)
            item_path = '/'.join(parts[1:])
        if item_path == '':
            item_path = 'index.html'
        return identifier, item_path

    def GET(self, request_path):
        identifier, item_path = self.get_identifier_and_item_path(web, request_path)
        item_base_url = lookup_item_base_url(identifier, None)
        if item_base_url:
            proxy_url = item_base_url + '/' + item_path
            web.header('x-accel-redirect', "/xaccel/" + proxy_url)
            return
        else:
            return 'Not found'


if __name__ == "__main__":
    app.run()
