"""
    sphinx-simulink.directives
    ~~~~~~~~~~~~~~~~~~~~~~~

    Embed Simulink diagrams on your documentation.

    :copyright:
    Copyright 2016 by Dennis Edward Kalinowski <dekalinowski@gmail.com>.

    :license:
    MIT, see LICENSE for details.

"""

import hashlib
import os
import tempfile

from docutils.parsers.rst import directives
from docutils.parsers.rst.directives import images

from sphinx.util.osutil import ensuredir

from sphinxsimulink.diagram import nodes


def pathlist(argument):

    paths = []

    list = argument.split(';')
    for path in list:
        paths.append( directives.path(path) )

    return paths


class SimulinkDiagramDirective(images.Figure):

    required_arguments = 1
    optional_arguments = 0

    option_spec = dict(
        images.Figure.option_spec, **{
            'dir': directives.path,
            'addpath': pathlist,
            'preload': directives.path,
            'subsystem': directives.unchanged,
        }
    )

    # content used by images.Figure as caption
    has_content = True

    @staticmethod
    def generate_uri(app, diagram_options, fileformat):

        # give a unique folder name for the specific srcdir, housed under the
        # system's temporary directory
        outdir = os.path.join(
            tempfile.gettempdir(),
            'sphinxsimulink',
            hashlib.sha1(
                os.path.abspath( app.builder.srcdir ).encode('utf-8')
            ).hexdigest()
        )

        # FIXME: change filename hash to include contents of preload script,
        # simulink system model, and other dependencies...
        # use as mechanism to reuse cache, and delete on clean job

        # make a unique filename for the Simulink model
        hash = hashlib.sha1( repr( sorted( diagram_options.items() ) )
            .encode('utf-8') ).hexdigest()
        filename = "simulink-diagram-{}.{}".format( hash, fileformat )

        # combine the directory and filename
        uri = os.path.join(outdir, filename)

        return uri

    def run(self):

        env = self.state.document.settings.env
        app = env.app

        # pop these keys out of self.options;
        # place into diagram_options
        diagram_options = dict(
            (popped_key, self.options.pop(popped_key, None))
            for popped_key in
            ('dir','addpath','preload','subsystem')
        )

        # generate image at this location; Sphinx will relocate later
        uri = SimulinkDiagramDirective.generate_uri(
            app, diagram_options, 'png'
        )

        # make an empty file, if needed, to avoid warning from Sphinx's image
        # processing
        ensuredir( os.path.dirname( uri ) )
        open( uri, 'a' ).close()

        # SimulinkDiagramDirective takes system from argument[0]
        system = self.arguments[0]

        # images.Figure expects uri in argument[0]
        self.arguments[0] = uri;
        (figure_node,) = images.Figure.run(self)

        # escalate system messages
        if isinstance(figure_node, nodes.system_message):
            return [figure_node]

        diagram_node = nodes.diagram('', figure_node, **diagram_options)
        diagram_node['uri'] = uri
        diagram_node['system'] = system

        return [diagram_node]


