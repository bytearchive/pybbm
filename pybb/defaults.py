# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os.path
import warnings
from collections import OrderedDict
from django.conf import settings
from django.utils.six import string_types
from django.utils.translation import ugettext as _

PYBB_TOPIC_PAGE_SIZE = getattr(settings, 'PYBB_TOPIC_PAGE_SIZE', 10)
PYBB_FORUM_PAGE_SIZE = getattr(settings, 'PYBB_FORUM_PAGE_SIZE', 20)
PYBB_AVATAR_WIDTH = getattr(settings, 'PYBB_AVATAR_WIDTH', 80)
PYBB_AVATAR_HEIGHT = getattr(settings, 'PYBB_AVATAR_HEIGHT', 80)
PYBB_MAX_AVATAR_SIZE = getattr(settings, 'PYBB_MAX_AVATAR_SIZE', 1024 * 50)
PYBB_DEFAULT_TIME_ZONE = getattr(settings, 'PYBB_DEFAULT_TIME_ZONE', 3)

PYBB_SIGNATURE_MAX_LENGTH = getattr(settings, 'PYBB_SIGNATURE_MAX_LENGTH', 1024)
PYBB_SIGNATURE_MAX_LINES = getattr(settings, 'PYBB_SIGNATURE_MAX_LINES', 3)

PYBB_DEFAULT_MARKUP = getattr(settings, 'PYBB_DEFAULT_MARKUP', 'bbcode')
PYBB_FREEZE_FIRST_POST = getattr(settings, 'PYBB_FREEZE_FIRST_POST', False)

PYBB_ATTACHMENT_SIZE_LIMIT = getattr(settings, 'PYBB_ATTACHMENT_SIZE_LIMIT', 1024 * 1024)
PYBB_ATTACHMENT_ENABLE = getattr(settings, 'PYBB_ATTACHMENT_ENABLE', False)
PYBB_ATTACHMENT_UPLOAD_TO = getattr(settings, 'PYBB_ATTACHMENT_UPLOAD_TO', os.path.join('pybb_upload', 'attachments'))

PYBB_DEFAULT_AVATAR_URL = getattr(settings, 'PYBB_DEFAULT_AVATAR_URL',
                                  getattr(settings, 'STATIC_URL', '') + 'pybb/img/default_avatar.jpg')

PYBB_DEFAULT_TITLE = getattr(settings, 'PYBB_DEFAULT_TITLE', 'PYBB Powered Forum')

PYBB_SMILES_PREFIX = getattr(settings, 'PYBB_SMILES_PREFIX', 'pybb/emoticons/')

PYBB_SMILES = getattr(settings, 'PYBB_SMILES', {
    '&gt;_&lt;': 'angry.png',
    ':.(': 'cry.png',
    'o_O': 'eyes.png',
    '[]_[]': 'geek.png',
    '8)': 'glasses.png',
    ':D': 'lol.png',
    ':(': 'sad.png',
    ':O': 'shok.png',
    '-_-': 'shy.png',
    ':)': 'smile.png',
    ':P': 'tongue.png',
    ';)': 'wink.png'
})

# TODO In a near future, this code will be deleted when callable settings will not supported anymore.
warning = _('%(setting_name)s should not be a callable anymore but a path to the parser classes.'
            'ex : myproject.markup.CustomBBCodeParser')


def getsetting_with_deprecation_check(all_settings, setting_name):
    setting_value = getattr(all_settings, setting_name)
    values = setting_value if type(setting_value) is not dict else setting_value.values()
    for value in values:
        if isinstance(value, string_types):
            continue
        warnings.warn(
            warning % {'setting_name': setting_name, },
            DeprecationWarning
        )
    return setting_value


if not hasattr(settings, 'PYBB_MARKUP_ENGINES'):
    PYBB_MARKUP_ENGINES = {'bbcode': 'pybb.markup.BBCodeParser',
                           'markdown': 'pybb.markup.MarkdownParser'}
else:
    PYBB_MARKUP_ENGINES = getsetting_with_deprecation_check(settings, 'PYBB_MARKUP_ENGINES')

if not hasattr(settings, 'PYBB_QUOTE_ENGINES'):
    PYBB_QUOTE_ENGINES = {'bbcode': 'pybb.markup.BBCodeParser',
                          'markdown': 'pybb.markup.MarkdownParser'}
else:
    PYBB_QUOTE_ENGINES = getsetting_with_deprecation_check(settings, 'PYBB_QUOTE_ENGINES')

PYBB_MARKUP = getattr(settings, 'PYBB_MARKUP', None)
if not PYBB_MARKUP or PYBB_MARKUP not in PYBB_MARKUP_ENGINES:
    if not PYBB_MARKUP_ENGINES:
        PYBB_MARKUP = None
    elif 'bbcode' in PYBB_MARKUP_ENGINES:
        # Backward compatibility. bbcode is the default markup
        PYBB_MARKUP = 'bbcode'
    else:
        # If a developer define his own markups without specifing default,
        # auto choose the first one in alphabetical order
        PYBB_MARKUP = OrderedDict(PYBB_MARKUP_ENGINES).keys()[0]

PYBB_TEMPLATE = getattr(settings, 'PYBB_TEMPLATE', "base.html")
PYBB_DEFAULT_AUTOSUBSCRIBE = getattr(settings, 'PYBB_DEFAULT_AUTOSUBSCRIBE', True)
PYBB_ENABLE_ANONYMOUS_POST = getattr(settings, 'PYBB_ENABLE_ANONYMOUS_POST', False)
PYBB_ANONYMOUS_USERNAME = getattr(settings, 'PYBB_ANONYMOUS_USERNAME', 'Anonymous')
PYBB_ANONYMOUS_VIEWS_CACHE_BUFFER = getattr(settings, 'PYBB_ANONYMOUS_VIEWS_CACHE_BUFFER', 100)

PYBB_PREMODERATION = getattr(settings, 'PYBB_PREMODERATION', False)

if not hasattr(settings, 'PYBB_BODY_CLEANERS'):
    PYBB_BODY_CLEANERS = ['pybb.markup.rstrip_str', 'pybb.markup.filter_blanks']
else:
    PYBB_BODY_CLEANERS = getsetting_with_deprecation_check(settings, 'PYBB_BODY_CLEANERS')

PYBB_BODY_VALIDATOR = getattr(settings, 'PYBB_BODY_VALIDATOR', None)

PYBB_POLL_MAX_ANSWERS = getattr(settings, 'PYBB_POLL_MAX_ANSWERS', 10)

PYBB_AUTO_USER_PERMISSIONS = getattr(settings, 'PYBB_AUTO_USER_PERMISSIONS', True)

PYBB_USE_DJANGO_MAILER = getattr(settings, 'PYBB_USE_DJANGO_MAILER', False)

PYBB_PERMISSION_HANDLER = getattr(settings, 'PYBB_PERMISSION_HANDLER', 'pybb.permissions.DefaultPermissionHandler')

PYBB_PROFILE_RELATED_NAME = getattr(settings, 'PYBB_PROFILE_RELATED_NAME', 'pybb_profile')

PYBB_INITIAL_CUSTOM_USER_MIGRATION = getattr(settings, 'PYBB_INITIAL_CUSTOM_USER_MIGRATION', None)

# Backward compatibility : define old functions which was defined here if some devs did used it
# TODO in a near future : delete those functions

def bbcode(s):
    warnings.warn('pybb.defaults.bbcode function is deprecated. Use pybb.markup.BBCodeParser instead.',
                  DeprecationWarning)
    from pybb.markup import BBCodeParser
    return BBCodeParser().format(s)

def markdown(s):
    warnings.warn('pybb.defaults.markdown function is deprecated. Use pybb.markup.MarkdownParser instead.',
                  DeprecationWarning)
    from pybb.markup import MarkdownParser
    return MarkdownParser().format(s)

def _render_quote(name, value, options, parent, context):
    warnings.warn('pybb.defaults._render_quote function is deprecated. '
                  'This function is internal of new pybb.markup.BBCodeParser class.',
                  DeprecationWarning)
    from pybb.markup import BBCodeParser
    return BBCodeParser()._render_quote(name, value, options, parent, context)

def smile_it(s):
    warnings.warn('pybb.defaults.smile_it function is deprecated. Use pybb.markup.smile_it instead.',
                  DeprecationWarning)
    from pybb.markup import smile_it as real_smile_it
    return real_smile_it(s)
