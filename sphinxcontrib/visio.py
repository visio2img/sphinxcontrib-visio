from docutils import nodes
from docutils.parsers.rst import directives
from docutils.parsers.rst import Directive
from docutils.parsers.rst.directives.images import Image
from visio2img.visio2img import export_img
import os.path
from os import stat
from sys import stderr
from hashlib import md5
from time import time
from datetime import datetime


def obtain_general_image_filename(visio_filename, **options):
    m = md5()
    m.update((visio_filename + str(options)).encode())
    h = m.hexdigest()   # h means hash
    return os.path.join(os.path.dirname(visio_filename), h) + '.png'


class visio_image(nodes.General, nodes.Element):
    pass


class VisioImage(Image):
    option_spec = Image.option_spec.copy()
    option_spec['page'] = directives.nonnegative_int
    option_spec['name'] = directives.unchanged

    def run(self):
        pagenum = self.options.pop('page', None)
        pagename = self.options.pop('name', None)

        result = super(VisioImage, self).run()
        if isinstance(result[0], nodes.image):
            image = visio_image(filename=self.arguments[0],
                                pagenum=pagenum,
                                pagename=pagename,
                                **result[0].attributes)
            result[0] = image
        else:
            for node in result[0].traverse(nodes.image):
                image = visio_image(filename=self.arguments[0],
                                    pagenum=pagenum,
                                    pagename=pagename,
                                    **node[0].attributes)
                node.replace_self(image)

        return result


def on_doctree_resolved(app, doctree, docname):
    for node in doctree.traverse(visio_image):
        image_filename = obtain_general_image_filename(os.path.join(app.outdir, node['filename']),
                                                       **node.attributes)
        image_pathname = os.path.abspath(image_filename)
        last_modified = os.stat(node['filename']).st_mtime

        if not os.path.exists(image_pathname) or os.stat(image_pathname).st_mtime < last_modified:
            visio_pathname = os.path.abspath(node['filename'])
            export_img(visio_pathname, image_pathname, node['pagenum'], node['pagename'])

        reference = directives.uri(os.path.basename(image_filename))
        image_node = nodes.image(candidates={'*': os.path.basename(image_filename)},
                                 **node.attributes)
        image_node['uri'] = reference
        node.replace_self(image_node)


def setup(app):
    app.add_directive('visio', VisioImage)
    app.connect('doctree-resolved', on_doctree_resolved)
