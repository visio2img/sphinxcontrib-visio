from docutils import nodes
from docutils.parsers.rst import directives
from docutils.parsers.rst import Directive
from docutils.parsers.rst.directives.images import Image
from visio2img import visio2img
from sphinx.util.osutil import ensuredir
import os.path
from os import stat
from sys import stderr
from hashlib import sha1
from time import time
from datetime import datetime


class visio_image(nodes.General, nodes.Element):
    def convert_to(self, filename, builder):
        try:
            visio_pathname = os.path.abspath(self['filename'])
            image_filename = os.path.abspath(filename)

            ensuredir(os.path.dirname(image_filename))
            visio2img.export_img(visio_pathname, image_filename,
                                 self['pagenum'], self['pagename'])
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
        if builder.format == 'html':
            reldir = "_images"
            outdir = os.path.join(builder.outdir, '_images')
        else:
            reldir = ""
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
        filename = self.arguments[0]
        pagenum = self.options.pop('page', None)
        pagename = self.options.pop('name', None)

        if not os.path.exists(filename):
            raise self.warning('visio file not found: %s' % filename)

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
                                    **node[0].attributes)
                node.replace_self(image)

        return result


def on_doctree_resolved(app, doctree, docname):
    for visio in doctree.traverse(visio_image):
        image_node = visio.to_image(app.builder)
        visio.replace_self(image_node)


def setup(app):
    app.add_directive('visio', VisioImage)
    app.connect('doctree-resolved', on_doctree_resolved)
