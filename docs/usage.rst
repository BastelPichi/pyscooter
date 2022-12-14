Usage
=====

.. _installation:

Installation
------------

To use pyscooter, first install it using pip:

.. code-block:: console

   $ pip install pyscooter


.. note::
    
    The pip version may be a few commits behind.



Importing
---------
Each provider has its own file in the ``providers`` folder. We try to keep the functions of each provider similar, however this is often difficult as the APIs are different.

For example for Bolt:

   >>> from pyscooter.providers.bolt import Bolt

.. note::
   
    Bolt is currently the only suported provider. Others soon to come.
    


The classes often have different methods and different init parameters. Please take a look at the individual documents.
