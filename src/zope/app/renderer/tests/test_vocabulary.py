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
"""Tests for Renderer Vocabulary.


"""
import unittest

from zope.component.interfaces import IFactory
from zope.component.testing import PlacelessSetup
from zope.schema.interfaces import IVocabulary
from zope.schema.interfaces import IVocabularyTokenized

from zope import component as ztapi
from zope.app.renderer import SourceFactory
from zope.app.renderer.interfaces import ISource
from zope.app.renderer.vocabulary import SourceTypeVocabulary


class IFoo(ISource):
    """Source marker interface"""


FooFactory = SourceFactory(IFoo, 'Foo', 'Foo Source')


class IFoo2(ISource):
    """Source marker interface"""


Foo2Factory = SourceFactory(IFoo2, 'Foo2', 'Foo2 Source')

# The vocabulary uses SimpleVocabulary now, so these tests are a bit
# redundant.  Leaving them in as confirmation that the replacement function
# works identically to the old custom vocabulary.


class SourceTypeVocabularyTest(PlacelessSetup, unittest.TestCase):

    def setUp(self):
        super().setUp()
        ztapi.provideUtility(FooFactory, IFactory, 'zope.source.Foo')
        ztapi.provideUtility(Foo2Factory, IFactory, 'zope.source.Foo2')
        self.vocab = SourceTypeVocabulary(None)

    def test_Interface(self):
        self.assertTrue(IVocabulary.providedBy(self.vocab))
        self.assertTrue(IVocabularyTokenized.providedBy(self.vocab))

    def test_contains(self):
        self.assertIn('zope.source.Foo', self.vocab)
        self.assertNotIn('zope.source.Foo3', self.vocab)

    def test_iter(self):
        self.assertIn(
            'zope.source.Foo', [term.value for term in self.vocab])
        self.assertNotIn(
            'zope.source.Foo3', [term.value for term in iter(self.vocab)])

    def test_len(self):
        self.assertEqual(len(self.vocab), 2)

    def test_getTerm(self):
        self.assertEqual(self.vocab.getTerm('zope.source.Foo').title, 'Foo')
        self.assertRaises(
            LookupError, self.vocab.getTerm, ('zope.source.Foo3',))

    def test_getTermByToken(self):
        vocab = self.vocab
        self.assertEqual(vocab.getTermByToken('zope.source.Foo').title, 'Foo')
        self.assertRaises(
            LookupError, vocab.getTermByToken, ('zope.source.Foo3',))


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)


if __name__ == '__main__':
    unittest.main()
