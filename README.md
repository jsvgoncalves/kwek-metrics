# Kwek Metrics

See aggregated metrics of your OpenShift projects. Customize with multiple OpenShift instances and different metrics.

## Development

To setup your virtualenv:

    $ mkvirtualenv kwek
    $ setvirtualenvproject kwek path_to_project

    # Optionally, create a new project with
    $ mkproject kwek
    $ git clone git@github.com:jsvgoncalves/kwek-metrics .

Then, every time you work on the project, run:

    $ workon kwek

To install the dependencies run:

    $ pip install -r requirements.txt

And development dependencies:

    $ pip install -r requirements-dev.txt

## Front-end

Make sure you have all front-end development dependencies installed:

    $ npm install

To enter watch mode on gulp:

    $ gulp watch

### Virtualenvwrapper cheatsheet

    # To stop working
    $ deactivate
    # To show all environments
    $ workon
    # To show installed packages
    $ lssitepackages
