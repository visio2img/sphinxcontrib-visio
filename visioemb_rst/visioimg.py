from docutils import nodes
from docutils.parsers.rst import directives
from docutils.parsers.rst import Directive

from visio2img import export_img
import os.path
from sys import stderr


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
                   'align': align,
                   'page': directives.nonnegative_int,
                   'name': lambda arg: arg
                   }
    has_content = False

    def run(self):
        try:
            d_img_opts = self.options
            
            # for name option
            page_name = None
            if 'name' in d_img_opts:
                page_name = d_img_opts['name']
                print('namein')
                del(d_img_opts['name'])

            # for page option
            page_num = None
            if 'page' in d_img_opts:
                page_num = d_img_opts['page']
                print('page in')
                del(d_img_opts['page'])


            visio_filename = self.arguments[0]
            gen_img_filename = os.path.splitext(self.arguments[0])[0] + '.png'
            gen_img_filename = os.path.abspath(gen_img_filename)
            try:
                try:
                    print(
                        'export_img({vis}, {gen}, page_num={num}, '
                        'page_name={name})'.format(vis=visio_filename,
                            gen=gen_img_filename, 
                            num=page_num,
                            name=page_name)
                    )
                    export_img(visio_filename, gen_img_filename,
                            page_num=page_num,
                            page_name=page_name)
                except Exception as err:
                    print(err)
                    stderr.write('Exporting Error')
            except Exception as err:
                err_text = err.__class__.__name__
                err_text += str(err)
                stderr,write(err_text)
                raise self.error(err_text)

            reference = directives.uri(gen_img_filename)
            self.options['uri'] = reference
            
            image_node = nodes.image(rawsource=self.block_text,
                                     **d_img_opts)
            return [image_node]
        except Exception as err:
            stderr.write(err)
            return []
