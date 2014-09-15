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
