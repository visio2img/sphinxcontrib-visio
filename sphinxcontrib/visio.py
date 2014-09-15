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
            pagename = self.options.pop('name', None)
            pagenum = self.options.pop('page', None)

            visio_filename = self.arguments[0]
            gen_img_filename = obtain_general_image_filename(visio_filename,
                                                             page_num=pagenum)
            gen_img_filename = os.path.abspath(gen_img_filename)
            obtain_timestamp = lambda fname:    \
                datetime.fromtimestamp(stat(fname).st_mtime)
            if not os.path.exists(gen_img_filename) or (
                    obtain_timestamp(visio_filename) > (
                        obtain_timestamp(gen_img_filename))):
                print(
                    'export_img({vis}, {gen}, page_num={num}, '
                    'page_name={name})'.format(vis=visio_filename,
                                               gen=gen_img_filename,
                                               num=pagenum,
                                               name=pagename)
                )
                export_img(visio_filename, gen_img_filename, pagenum, pagename)

            reference = directives.uri(gen_img_filename)
            self.options['uri'] = reference

            image_node = nodes.image(rawsource=self.block_text,
                                     **self.options)
            return [image_node]
        except Exception as err:
            err_text = err.__class__.__name__
            err_text += str(err)
            stderr.write(err_text)
            raise self.error(err_text)


def setup(app):
    app.add_directive('visio', VisioImage)
