==============================================================================
sphinx-simulink
==============================================================================

Python Sphinx plugin to include MATLAB Simulink models (e.g. diagrams or
information) into .rst documentation

Dependencies
------------------------------------------------------------------------------

Sphinx (see http://www.sphinx-doc.org)
matlab.engine (see MathWorks documentation, first introduced in R2014B)

Usage
------------------------------------------------------------------------------

(todo: text description for below)

.. code-block:: rest

    .. simulink-diagram:: SimulinkModelName
        :dir: optional/path/to/model
        :addpath: optional/dependency/paths;support/list/of/directories;C:/absolute/paths/as/well
        :preload: preload_script.m
        :subsystem: SubsystemLayerInModel

TODO
------------------------------------------------------------------------------

Just finished a working version after a day's work... Need to clean up:

#. Finish README
#. Include example model input and output diagram
#. Create Python package
#. Change image filename hash to include contents of Simulink and preload script (dependencies as well?) -- this will help trigger refresh of diagrams
#. Delete the cached render image from the temporary directory, whenever running "clean" in Sphinx


