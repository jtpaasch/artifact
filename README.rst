Artifact
========

A simple tool to deploy AWS artifacts in ye olde Amazon cloud.

In development right now.


Setup
-----

The {{artifact}} scripts use {{Boto3}} to connect to Amazon, so you
need an Amazon profile file on your computer just as you would for
any other {{Boto3}} projecct.

I install and use this tool inside a virtual environment. For instance,
suppose this repo resides at {{~/code/repo}}, I then create a folder
where I can use this in a virtual environment::

    mkdir ~/artifact_test
    cd ~/artifact_test
    pyvenv venv
    . venv/bin/activate
    pip install ~/artifact --editable

Then I can use the {{stats}} and {{artifact}} scripts.
