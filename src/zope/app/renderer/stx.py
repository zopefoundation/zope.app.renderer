##############################################################################
#
# Copyright (c) 2003 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Structured Text Renderer Classes

"""
__docformat__ = 'restructuredtext'

import re

from zope.component import adapter
from zope.interface import implementer
from zope.publisher.browser import BrowserView
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.structuredtext.document import Document
from zope.structuredtext.html import HTML

from zope.app.renderer import SourceFactory
from zope.app.renderer.i18n import ZopeMessageFactory as _
from zope.app.renderer.interfaces import IHTMLRenderer
from zope.app.renderer.interfaces import ISource


class IStructuredTextSource(ISource):
    """Marker interface for a structured text source. Note that an
    implementation of this interface should always derive from unicode or
    behave like a unicode class."""


StructuredTextSourceFactory = SourceFactory(
    IStructuredTextSource, _("Structured Text (STX)"),
    _("Structured Text (STX) Source"))


@implementer(IHTMLRenderer)
@adapter(IStructuredTextSource, IBrowserRequest)
class StructuredTextToHTMLRenderer(BrowserView):
    r"""A view to convert from Plain Text to HTML.

    Example::

      >>> from zope.app.renderer import text_type
      >>> from zope.publisher.browser import TestRequest
      >>> source = StructuredTextSourceFactory(u'This is source.')
      >>> renderer = StructuredTextToHTMLRenderer(source, TestRequest())
      >>> rendered = renderer.render()
      >>> isinstance(rendered, text_type)
      True
      >>> print(rendered)
      <p>This is source.</p>
      <BLANKLINE>

    Make sure that unicode works as well::

      >>> source = StructuredTextSourceFactory(u'This is \xc3\x9c.')
      >>> renderer = StructuredTextToHTMLRenderer(source, TestRequest())
      >>> rendered = renderer.render()
      >>> isinstance(rendered, text_type)
      True
      >>> print(rendered)
      <p>This is ...</p>
      <BLANKLINE>
    """

    def render(self):
        "See zope.app.interfaces.renderer.IHTMLRenderer"

        doc = Document()(self.context)
        html = HTML()(doc)

        # strip html & body added by some zope versions
        html = re.sub(
            r'(?sm)^<html.*<body.*?>\n(.*)</body>\n</html>\n',
            r'\1',
            html)

        return html
