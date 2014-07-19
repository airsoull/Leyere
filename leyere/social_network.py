# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

import tweepy

from leyere.goog_gl import shorturl

def update_social_network(user, provider, url):
    social_auth = user.social_auth.filter(provider=provider).latest('pk')
    access_token, access_token_secret = __get_tokens(social_auth.tokens)

    consumer_key = settings.SOCIAL_AUTH_TWITTER_KEY
    consumer_secret = settings.SOCIAL_AUTH_TWITTER_SECRET

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)
    text = '%s %s %s %s' % (unicode(_(u'Acabo de publicar una historía')), shorturl(url), unicode(_(u'vía')), '@LeyereCom')
    api.update_status(text)

def __get_tokens(tokens):
    if isinstance(tokens, dict):
        return tokens['oauth_token'], tokens['oauth_token_secret']
    temp_tokens = {}
    for pair in tokens.split('&'):
        key, value = pair.split('=')
        temp_tokens[key] = value
    return temp_tokens['oauth_token'], temp_tokens['oauth_token_secret']