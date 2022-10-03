Usage
=====

.. _installation:

Installation
------------

To use Lumache, first install it using pip:

.. code-block:: console

   $ pip install pyscooter


.. note::
    
    The library isn't finished yet. Please download the appropiate file from the provider folder manually, or wait for the relase. The pip version is empty



Importing
---------
Each provider has its own file in the ``providers`` folder. We trie to keep the functions of each provider similar, however this is often difficult as the APIs are different.

For example for Bolt:

   >>> from pyscooter.providers.bolt import Bolt

.. note::
   
    Bolt is currently the only suported provider. Others soon to come.
    


The class then has different methods and different init parameters. Please take a look at the individual documents.

.. toctree::

   providers
