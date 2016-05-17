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

import pkg_resources
from hashlib import sha1
from docutils.parsers.rst import directives
from visio2img.visio2img import (
    VisioFile, filter_pages, is_pywin32_available
)
from sphinxcontrib.imagehelper import (
    ImageConverter, add_image_type, add_image_directive, add_figure_directive
)


class VisioConverter(ImageConverter):
    option_spec = {
        'page': directives.nonnegative_int,
        'sheet': directives.unchanged,
    }

    def get_filename_for(self, node):
        options = dict(uri=node['uri'], page=node.get('page'), name=node.get('sheet'))
        hashed = sha1(str(options).encode('utf-8')).hexdigest()
        return "visio-%s.png" % hashed

    def convert(self, node, filename, to):
        if not is_pywin32_available():
            self.app.env.warn_node('Fail to convert visio image: win32com not installed',
                                   node)
            return False

        try:
            with VisioFile.Open(filename) as visio:
                pages = filter_pages(visio.pages, node.get('page'), node.get('sheet'))
                if len(pages) > 1:
                    msg = ('visio file [%s] contains multiple pages. '
                           'specify :page: or :name: option.')
                    self.app.warn(msg % node['uri'])
                    return False

                pages[0].Export(to)
                return True
        except Exception as exc:
            self.app.warn('Fail to convert visio image: %s' % exc)
            return False


def setup(app):
    add_image_type(app, 'visio', ('vsd', 'vsdx'), VisioConverter)
    add_image_directive(app, 'visio', VisioConverter.option_spec)
    add_figure_directive(app, 'visio', VisioConverter.option_spec)

    return {
        'version': pkg_resources.require('sphinxcontrib-visio')[0].version,
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
