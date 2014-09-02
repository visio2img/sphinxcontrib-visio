from docutils import nodes
from docutils.parsers.rst import directives
from docutils.parsers.rst import Directive

from visio2img import export_img
print('installed ...')
import os.path



def setup(builder):
    directives.register_directive('visioimg', VisioImage)

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
                   'align': align
                   }
    has_content = False

    def run(self):
        try:
            print('running ...')
            visio_filename = self.arguments[0]
            gen_img_filename = os.path.splitext(self.arguments[0])[0] + '.png'
            gen_img_filename = os.path.abspath(gen_img_filename)
            try:
                try:
                    export_img(visio_filename, gen_img_filename, page_num=1)
                except Exception as err:
                    print('Exporting Error')
                print('Export ...')
            except Exception as err:
                err_text = err.__class__.__name__
                err_text += str(err)
                print(err_text)
                raise self.error(err_text)

            reference = directives.uri(gen_img_filename)
            self.options['uri'] = reference
            image_node = nodes.image(rawsource=self.block_text,
                                     **self.options)
            return [image_node]
        except Exception as err:
            print(err)
            return []
