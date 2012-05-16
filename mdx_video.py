#!/usr/bin/env python

"""
Embeds web videos using URLs.  For instance, if a URL to an youtube video is
found in the text submitted to markdown and it isn't enclosed in parenthesis
like a normal link in markdown, then the URL will be swapped with a embedded
youtube video.

All resulting HTML is XHTML Strict compatible.

>>> import markdown

Test Youku video

>>> s = "http://v.youku.com/v_show/id_XMjkzOTc5MzQw.html"
>>> markdown.markdown(s, extensions=['video'])
u'<p><object data="http://player.youku.com/player.php/sid/XMjkzOTc5MzQw/v.swf" height="400" type="application/x-shockwave-flash" width="480"><param name="movie" value="http://player.youku.com/player.php/sid/XMjkzOTc5MzQw/v.swf"></param><param name="allowFullScreen" value="true"></param><embed allowFullScreen="true" height="400" src="http://player.youku.com/player.php/sid/XMjkzOTc5MzQw/v.swf" type="application/x-shockwave-flash" width="480"></embed></object></p>'

Test Tudou video

>>> s = "http://www.tudou.com/programs/view/6K89f_CqbYw/"
>>> markdown.markdown(s, extensions=['video'])
u'<p><object data="http://www.tudou.com/v/6K89f_CqbYw/v.swf" height="400" type="application/x-shockwave-flash" width="480"><param name="movie" value="http://www.tudou.com/v/6K89f_CqbYw/v.swf"></param><param name="allowFullScreen" value="true"></param><embed allowFullScreen="true" height="400" src="http://www.tudou.com/v/6K89f_CqbYw/v.swf" type="application/x-shockwave-flash" width="480"></embed></object></p>'
"""

import markdown
try:
    from markdown.util import etree
except:
    from markdown import etree

version = "0.1.6"


class VideoExtension(markdown.Extension):

    def __init__(self, configs):
        self.config = {
            'youku_width': ['480', 'Width for Youku videos'],
            'youku_height': ['400', 'Height for Youku videos'],
            'tudou_width': ['480', 'Width for Tudou videos'],
            'tudou_height': ['400', 'Height for Tudou videos'],
        }

        # Override defaults with user settings
        for key, value in configs:
            self.setConfig(key, value)


    def add_inline(self, md, name, klass, re):
        pattern = klass(re)
        pattern.md = md
        pattern.ext = self
        md.inlinePatterns.add(name, pattern, "<reference")


    def extendMarkdown(self, md, md_globals):
        self.add_inline(md, 'youku', Youku,
            r'([^(]|^)http://v\.youku\.com/v_show/id_(?P<youkuvid>\w+).html')
        self.add_inline(md, 'tudou', Tudou,
            r'([^(]|^)http://www\.tudou\.com/programs/view/(?P<tudouvid>\w+)/\S*')


class Youku(markdown.inlinepatterns.Pattern):

    def handleMatch(self, m):
        url = "http://player.youku.com/player.php/sid/%s/v.swf" % m.group('youkuvid')
        width = self.ext.config['youku_width'][0]
        height = self.ext.config['youku_height'][0]
        obj = flash_object(url, width, height)
        # might append some site specific params to obj here
        return obj


class Tudou(markdown.inlinepatterns.Pattern):

    def handleMatch(self, m):
        url = "http://www.tudou.com/v/%s/v.swf" % m.group('tudouvid')
        width = self.ext.config['tudou_width'][0]
        height = self.ext.config['tudou_height'][0]
        obj = flash_object(url, width, height)
        return obj


def flash_object(url, width, height):
    obj = etree.Element('object')
    obj.set('type', 'application/x-shockwave-flash')
    obj.set('width', width)
    obj.set('height', height)
    obj.set('data', url)
    param = etree.Element('param')
    param.set('name', 'movie')
    param.set('value', url)
    obj.append(param)
    param = etree.Element('param')
    param.set('name', 'allowFullScreen')
    param.set('value', 'true')
    obj.append(param)
    embed = etree.Element('embed')
    embed.set('type', 'application/x-shockwave-flash')
    embed.set('width', width)
    embed.set('height', height)
    embed.set('src', url)
    embed.set('allowFullScreen', 'true')
    obj.append(embed)
    return obj


def makeExtension(configs=None) :
    return VideoExtension(configs=configs)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
