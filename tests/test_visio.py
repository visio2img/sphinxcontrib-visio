# -*- coding: utf-8 -*-

import unittest
from time import time
from sphinx_testing import with_app
from sphinx_testing.path import path


class TestSphinxcontribBlockdiagHTML(unittest.TestCase):
    @with_app(buildername='html', srcdir="tests/examples/basic", copy_srcdir_to_tmpdir=True)
    def test_visio(self, app, status, warnings):
        # first build
        app.build()
        print status.getvalue(), warnings.getvalue()
        html = (app.outdir / 'index.html').read_text()
        image_files = (app.outdir / '_images').listdir()
        self.assertEqual(1, len(image_files))
        image_filename = image_files[0]

        self.assertRegexpMatches(html, '<img alt="(_images\\\\%s)" src="\\1" />' % image_filename)

        expected = path("tests/examples/singlepage.png").read_bytes()
        actual = (app.outdir / '_images' / image_filename).read_bytes()
        self.assertEqual(expected, actual)

        # second build (no updates)
        status.truncate(0)
        warnings.truncate(0)
        app.build()

        self.assertIn('0 added, 0 changed, 0 removed', status.getvalue())

        # thrid build (.vsdx file has changed)
        status.truncate(0)
        warnings.truncate(0)
        (app.srcdir / 'singlepage.vsdx').utime((time(), time()))
        app.build()

        self.assertIn('0 added, 1 changed, 0 removed', status.getvalue())

    @with_app(buildername='html', srcdir="tests/examples/subdir", copy_srcdir_to_tmpdir=True)
    def test_visio_in_subdir(self, app, status, warnings):
        # first build
        app.build()
        html = (app.outdir / 'subdir' / 'index.html').read_text()
        image_files = (app.outdir / '_images').listdir()
        self.assertEqual(1, len(image_files))
        image_filename = image_files[0]

        self.assertRegexpMatches(html, '<img alt="(\.\.\\\\_images\\\\%s)" src="\\1" />' % image_filename)

        expected = path("tests/examples/multipages-1.png").read_bytes()
        actual = (app.outdir / '_images' / image_filename).read_bytes()
        self.assertEqual(expected, actual)

    @with_app(buildername='html', srcdir="tests/examples/pagenum", copy_srcdir_to_tmpdir=True)
    def test_page_option(self, app, status, warnings):
        # first build
        app.build()
        html = (app.outdir / 'index.html').read_text()
        image_files = (app.outdir / '_images').listdir()
        self.assertEqual(1, len(image_files))
        image_filename = image_files[0]

        self.assertRegexpMatches(html, '<img alt="(_images\\\\%s)" src="\\1" />' % image_filename)

        expected = path("tests/examples/multipages-1.png").read_bytes()
        actual = (app.outdir / '_images' / image_filename).read_bytes()
        self.assertEqual(expected, actual)

    @with_app(buildername='html', srcdir="tests/examples/pagename", copy_srcdir_to_tmpdir=True)
    def test_name_option(self, app, status, warnings):
        # first build
        app.build()
        html = (app.outdir / 'index.html').read_text()
        image_files = (app.outdir / '_images').listdir()
        self.assertEqual(1, len(image_files))
        image_filename = image_files[0]

        self.assertRegexpMatches(html, '<img alt="(_images\\\\%s)" src="\\1" />' % image_filename)

        expected = path("tests/examples/multipages-2.png").read_bytes()
        actual = (app.outdir / '_images' / image_filename).read_bytes()
        self.assertEqual(expected, actual)
