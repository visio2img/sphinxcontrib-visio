from docutils import nodes
from docutils.parsers.rst import directives
from docutils.parsers.rst import Directive

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


def align(argument):
    """Conversion function for the "align" option."""
    return directives.choice(argument, ('left', 'center', 'right'))


class visio_image(nodes.General, nodes.Element):
    pass


class VisioImage(Directive):

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {'alt': directives.unchanged,
                   'height': directives.nonnegative_int,
                   'width': directives.nonnegative_int,
                   'scale': directives.nonnegative_int,
                   'align': align,
                   'page': directives.nonnegative_int,
                   'name': lambda arg: arg
                   }
    has_content = False

    def run(self):
        try:
            image_node = visio_image(filename=self.arguments[0],
                                     pagenum=self.options.pop('page', None),
                                     pagename=self.options.pop('name', None))
            return [image_node]
        except Exception as err:
            err_text = err.__class__.__name__
            err_text += str(err)
            stderr.write(err_text)
            raise self.error(err_text)


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
        image_node = nodes.image(candidates={'*': os.path.basename(image_filename)}, uri=reference)
        node.replace_self(image_node)


def setup(app):
    app.add_directive('visio', VisioImage)
    app.connect('doctree-resolved', on_doctree_resolved)
