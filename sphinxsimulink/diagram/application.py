"""
    sphinx-simulink.application
    ~~~~~~~~~~~~~~~~~~~~~~~

    Embed Simulink diagrams on your documentation.

    :copyright:
    Copyright 2016 by Dennis Edward Kalinowski <dekalinowski@gmail.com>.

    :license:
    MIT, see LICENSE for details.

"""

import matlab.engine
import os

from sphinx.errors import SphinxError
from sphinx.util.osutil import ensuredir

from sphinxsimulink.diagram import directives,nodes
from sphinxsimulink.metadata import __version__


engine = None


class SimulinkDiagramError(SphinxError):
    pass

def render_diagram(app, node, docname):

    global engine

    uri = node['uri']

    # do not regenerate
    if os.path.exists( uri ):
        pass

    ensuredir( os.path.dirname( uri ) )

    try:

        # reuse last engine to save loading time
        if engine == None:
            engine = matlab.engine.start_matlab()
        else:
            # clean up used engines
            engine.restoredefaultpath(nargout=0)
            engine.close('all', nargout=0)
            engine.bdclose('all', nargout=0)
            engine.clear('classes', nargout=0)

        # start engine from document directory
        engine.cd( os.path.dirname( app.env.doc2path( docname ) ) )

        # then, support changing directory (relative to document)
        dir = node.get('dir')
        if dir:
            engine.cd( dir )

        # finally, add the MATLAB paths relative to the changed directory
        pathlist = node.get('addpath')
        if pathlist:
            for path in pathlist:
                engine.addpath( path )

        # preload script
        preload = node.get('preload')
        if preload:
            engine.eval( preload + ';', nargout=0)

        # load system
        system = node.get('system')
        if system:
            engine.load_system( system );

        # if subsystem specified, print from this layer
        subsystem = node.get('subsystem')
        if subsystem:
            system = "/".join( [ system, subsystem ] )

        # print from Simulink handle to .png
        engine.eval(
            "print( get_param( '{}', 'Handle' ), '-dpng', '{}' )".
                format( system, uri ),
            nargout=0
            )

    except matlab.engine.MatlabExecutionError as err:
        raise SimulinkDiagramError('Unable to render Simulink diagram due ' +
            'to MATLAB execution error'
        )


def process_diagram_nodes(app, doctree, docname):

    for node in doctree.traverse(nodes.diagram):
        render_diagram(app, node, docname)
        node.replace_self(node.children)


def terminate_matlab_engine(app, exception):

    global engine

    if engine is not None:

        engine.quit()
        engine = None


def setup(app):

    app.add_directive('simulink-diagram', directives.SimulinkDiagramDirective)

    app.connect('doctree-resolved', process_diagram_nodes)
    app.connect('build-finished', terminate_matlab_engine)

    return {'version': __version__}


