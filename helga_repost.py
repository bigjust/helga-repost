import datetime
import humanize
import pymongo
import urllib
import urlparse

from collections import namedtuple

from helga import settings, log
from helga.db import db
from helga.plugins import match

CLEAN_UTM = getattr(settings, 'REPOST_REMOVE_UTM', False)

logger = log.getLogger(__name__)

def check_url(channel, nick, url):
    """
    Checks to see if url has been posted. If it has, report original
    poster and time since.

    returns either None if the link hasn't been seen before, or a
    tuple consisting of (original poster, time since)
    """

    db.repost.insert({
        'channel': channel,
        'nick': nick,
        'url': url,
        'timestamp': datetime.datetime.utcnow()
    })

    result_cursor = db.repost.find({
        'channel': channel,
        'url': url,
    }).sort([
        ('timestamp', pymongo.ASCENDING)
    ])

    results = list(result_cursor)

    if len(results) > 1:
        op = results[0]
        if op['nick'] == nick:
            # *points to temple*
            # can't be a repost if we're OP
            return

        now = datetime.datetime.utcnow()
        then = op['timestamp']
        return (op['nick'], humanize.naturaltime(now - then))

def clean_url(url):
    """
    if utm codes are present, removes them.
    """

    parsed_url = urlparse.urlparse(url)

    if parsed_url.query:
        dirty = False
        params_dict = urlparse.parse_qs(parsed_url.query)
        for key, value in params_dict.items():
            if key.startswith('utm_'):
                params_dict.pop(key)
                dirty = True

        if dirty:
            params = urllib.urlencode(params_dict, True)
            scheme, netloc, path, _, fragment = urlparse.urlsplit(url)
            url = urlparse.urlunsplit((scheme, netloc, path, params, fragment))

    return url

@match('https?://(\S*)')
def repost(client, channel, nick, message, matches):

    for match in matches:
        url = match
        if CLEAN_UTM:
            url = clean_url(match)
        logger.debug('url: {}'.format(url))

        repost = check_url(channel, nick, url)
        if repost:
            logger.debug('repost: {}'.format(repost))
            client.msg(
                channel,
                'REPOST: by {} {}'.format(
                    repost[0],
                    repost[1]
                ))

        if url != match:
            client.msg(channel, url)
