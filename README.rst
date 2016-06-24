==============================================================================
Simulink diagrams embedded in .rst documentation
==============================================================================

The ``simulink-diagram`` directive requires at minimum one argument specifying
the Simulink ``system``:

.. code-block:: rest

    .. simulink-diagram:: System

Additional options exist, including:

* ``dir``: the directory containing ``system``
* ``addpath``: one or more directories containing dependencies needed by the
  ``system`` (if multiple directories, use a semi-colon, e.g. path1;path2;path3)
* ``preload``: specify a MATLAB script file (.m) to load before opening the
  ``system`` for print
* ``subsystem``: the layer in the ``system`` to navigate and print from

Note: All directories may be specified either as relative to the .rst document
or an absolute path. If a list of directories, a mix of both may be employed.

.. code-block:: rest

    .. simulink-diagram:: System
        :dir: optional/path/to/model
        :addpath: optional/dependency/path;another/path/to/a/dependency;
            feel/free/to/split/across/lines;C:/And/With/Absolute/Paths
        :preload: optional_preload.m
        :subsystem: SubsystemLayerInModel/At/Any/Depth


Dependencies
------------------------------------------------------------------------------

Ensure you install the following into your Python environment:

* Sphinx (see http://www.sphinx-doc.org)
* matlab.engine (see MathWorks documentation, first introduced in R2014B)

Example
------------------------------------------------------------------------------

Please look in this repository's "example" folder for an example.


