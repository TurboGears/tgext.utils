# -*- coding: utf-8 -*-
from unittest import TestCase
from tgext.utils.meta import metatags


class TestMetaTags(TestCase):
    def test_single(self):
        self.assertEqual(
            metatags(title='My Title'),
            '''<meta property="og:title" content="My Title"/>
<meta name="twitter:title" content="My Title"/>
<meta itemprop="name" content="My Title"/>''')

    def test_all(self):
        self.assertEqual(
            metatags(title='My Title', description='My Descr', image='myimg', url='myurl'),
            '''<meta property="og:url" content="myurl"/>
<meta name="twitter:url" content="myurl"/>
<meta itemprop="url" content="myurl"/>
<meta property="og:image" content="myimg"/>
<meta name="twitter:image" content="myimg"/>
<meta itemprop="image" content="myimg"/>
<meta property="og:description" content="My Descr"/>
<meta name="twitter:description" content="My Descr"/>
<meta itemprop="description" content="My Descr"/>
<meta property="og:title" content="My Title"/>
<meta name="twitter:title" content="My Title"/>
<meta itemprop="name" content="My Title"/>''')

