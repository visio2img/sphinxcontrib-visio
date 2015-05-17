# -*- coding: utf-8 -*-
#  Copyright 2014 Yassu
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import os
from hashlib import sha1
from docutils import nodes
from docutils.parsers.rst import directives
from docutils.parsers.rst.directives.images import Image, Figure
from visio2img.visio2img import VisioFile, filter_pages
from sphinx.util.osutil import ensuredir


class visio_image(nodes.General, nodes.Element):
    def convert_to(self, filename, builder):
        try:
            with VisioFile.Open(self['filename']) as visio:
                pages = filter_pages(visio.pages,
                                     self['pagenum'],
                                     self['pagename'])
                if len(pages) > 1:
                    msg = ('visio file [%s] contains multiple pages. '
                           'specify :page: or :name: option.')
                    builder.warn(msg % self['filename'])
                    return False

                image_filename = os.path.abspath(filename)
                ensuredir(os.path.dirname(image_filename))
                pages[0].Export(image_filename)
                return True
        except Exception as exc:
            builder.warn('Fail to convert visio image: %s' % exc)
            return False

    def get_image_filename(self):
        options = dict(filename=self['filename'],
                       pagenum=self['pagenum'],
                       pagename=self['pagename'])
        hashed = sha1(str(options).encode('utf-8')).hexdigest()
        return "visio-%s.png" % hashed

    def to_image(self, builder):
        if hasattr(builder, 'imgpath'):  # Sphinx (<= 1.2.x) or HTML writer
            reldir = builder.imgpath
        else:
            reldir = ''

        if hasattr(builder, 'imagedir'):  # Sphinx (>= 1.3.x)
            outdir = os.path.join(builder.outdir, builder.imagedir)
        elif hasattr(builder, 'imgpath'):  # Sphinx (<= 1.2.x) and HTML writer
            outdir = os.path.join(builder.outdir, '_images')
        else:
            outdir = builder.outdir

        filename = self.get_image_filename()
        path = os.path.join(outdir, filename)
        last_modified = os.stat(self['filename']).st_mtime

        if not os.path.exists(path) or os.stat(path).st_mtime < last_modified:
            ret = self.convert_to(path, builder=builder)
            if ret:
                os.utime(path, (last_modified, last_modified))
            else:
                return nodes.Text('')

        relfn = os.path.join(reldir, filename)
        image_node = nodes.image(candidates={'*': relfn}, **self.attributes)
        image_node['uri'] = relfn

        return image_node


class VisioImage(Image):
    option_spec = Image.option_spec.copy()
    option_spec['page'] = directives.nonnegative_int
    option_spec['name'] = directives.unchanged

    def run(self):
        env = self.state.document.settings.env
        path = env.doc2path(env.docname, base=None)
        rel_filename = os.path.join(os.path.dirname(path), self.arguments[0])
        filename = os.path.join(env.srcdir, rel_filename)
        pagenum = self.options.pop('page', None)
        pagename = self.options.pop('name', None)

        if not os.path.exists(filename):
            raise self.warning('visio file not found: %s' % filename)

        env.note_dependency(rel_filename)
        result = super(VisioImage, self).run()
        if isinstance(result[0], nodes.image):
            image = visio_image(filename=filename,
                                pagenum=pagenum,
                                pagename=pagename,
                                **result[0].attributes)
            result[0] = image
        else:
            for node in result[0].traverse(nodes.image):
                image = visio_image(filename=filename,
                                    pagenum=pagenum,
                                    pagename=pagename,
                                    **node.attributes)
                node.replace_self(image)

        return result


class VisioFigure(Figure):
    option_spec = Figure.option_spec.copy()
    option_spec['page'] = directives.nonnegative_int
    option_spec['name'] = directives.unchanged

    def run(self):
        filename = self.arguments[0]
        pagenum = self.options.pop('page', None)
        pagename = self.options.pop('name', None)

        if not os.path.exists(filename):
            raise self.warning('visio file not found: %s' % filename)

        result = super(VisioFigure, self).run()
        for node in result[0].traverse(nodes.image):
            image = visio_image(filename=filename,
                                pagenum=pagenum,
                                pagename=pagename,
                                **node.attributes)
            node.replace_self(image)

        return result


def on_doctree_resolved(app, doctree, docname):
    for visio in doctree.traverse(visio_image):
        image_node = visio.to_image(app.builder)
        visio.replace_self(image_node)


def setup(app):
    app.add_directive('visio', VisioImage)
    app.add_directive('visio-image', VisioImage)
    app.add_directive('visio-figure', VisioFigure)
    app.connect('doctree-resolved', on_doctree_resolved)
