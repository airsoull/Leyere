import urllib2
import simplejson

def shorturl(urltoshorten):
    try:
        apiurl = "https://www.googleapis.com/urlshortener/v1/url"
        req = urllib2.Request(apiurl,
            headers={'Content-Type': 'application/json'},
            data='{{"longUrl": "{0}"}}'.format(urltoshorten))
        shorturl = simplejson.loads(urllib2.urlopen(req).read())['id']
    except:
        shorturl = urltoshorten
    return shorturl

if __name__ == "__main__":
    import doctest
    doctest.testmod()