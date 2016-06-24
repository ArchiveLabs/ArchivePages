import web
import urllib2
import internetarchive

urls = (
    '/(.*)', 'hello'
)
app = web.application(urls, globals())

config = dict(general=dict(secure=False))

def lookup_item(identifier, default):
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
    def GET(self, path):
        parts = path.split('/')
        key = parts[0]
        source = lookup_item(key, None)
        if source:
            relative_url = '/'.join(parts[1:])
            if relative_url == '':
                relative_url = 'index.html'
            url = source + '/' + relative_url
            web.header('x-accel-redirect', "/xaccel/" + url)
            return 'should not get here'
        else:
            return 'Not found'

if __name__ == "__main__":
    app.run()
