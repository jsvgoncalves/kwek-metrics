[//]: # (Aggregated Project Metrics For OpenShift)


_If you ever wanted to have an overview of how much resources all your projects and applications are using on OpenShift, read along!_


Kwek Metrics is a simple and effective web application that allows you to have an aggregated view for your projects' metrics. To immediately satisfy your curiosity, here's a screenshot of the web application.

![Kwek-Metrics](https://github.com/jsvgoncalves/kwek-metrics/raw/docs/docs/img/kwekoverview.png)


The next sections on this blog post will show you how to install and configure the web application, and, if you would need extra features, how to quickly get started on extending the code.

#### Contents
1. Installation
1.1 Clone the project
1.2 Install the required packages
2. Deploy to OpenShift
3. First configuration
3.1 Get your Service Key
3.2 Configure Kwek
4. Extending Kwek
4.1 Install development dependencies
4.2 Test the code
4.3 Run in development mode
5. Send in your patches!


<div class="alert alert-warning">
      <strong>Disclaimer:</strong> the project is still work in progress and at this moment it's shown here only with the intention of giving you an overview of how you could go about implementing a similar solution.
</div>


# 1. Installation

#### 1.1 Clone the project

In order to prevent dependency clashing for your Python projects, it's recommended to isolate each projects' dependencies in different places by using [Python Virtual Environments](http://docs.python-guide.org/en/latest/dev/virtualenvs/). In this case, we are using `virtualenvwrapper` which simplifies things for us a bit. So, to create a virtual environment and associate it directly with our project's folder, run:

```
$ mkproject kwek
```

This will automatically `cd` you into an empty `kwek/` directory.

Next, clone the project's git repository into the current folder:

```
$ git clone git@github.com:jsvgoncalves/kwek-metrics .
```
At this point you have your virtual environment set up and the project cloned, so you are almost ready to go.

You can find more information about installing and using `virtualenvwrapper` at [ virtualenvwrapper docs](http://virtualenvwrapper.readthedocs.io/en/latest/install.html). You can also find a [mini cheatsheet for virtualenvwrapper](https://github.com/jsvgoncalves/kwek-metrics#virtualenvwrapper-cheatsheet) on Kwek's GitHub repository.

#### 1.2 Install the required packages

In order to run the project, you need to install the required dependencies into your newly created virtual environment:

```
$ pip install -r requirements.txt
```

We also need to make sure that the the front-end dependencies are installed, so that we can build our assets. Those dependencies are declared on our `package.json`, so we simply need to run:

```
$ npm install
```

In our `package.json` we also specify the necessary commands to build and bundle our assets, so, for production mode, you need to run:

```
$ npm production
```

And this will bundle and minify our assets into the appropriate folders.

At this point, you are ready to run! So just run:

```
$ python app.py
* Running on http://127.0.0.1:8080/ (Press CTRL+C to quit)
```

If everything worked properly, you should be see the output as displayed above. So now just grab the link and let's go and configure `Kwek` with our OpenShift instance.

# 2. Deploy to OpenShift

Deploying Kwek to OpenShift is extremely easy, all you have to do is use the provided OpenShift template, which you can find at `openshift/kwek-metrics.json`. As usual, you can either use the web console or the terminal to create your application.

#### 2.1 Using the Web Console
On the Web Console, go to `Add To Project > Import YAML / JSON`:

![Import JSON](https://github.com/jsvgoncalves/kwek-metrics/raw/docs/docs/img/importjson.png)

Click the `Create` to finish the importing.

![Create App](https://github.com/jsvgoncalves/kwek-metrics/raw/docs/docs/img/createproject.png)

Then, optionally configure it according to your needs, i.e., replace the Git Repository URL with your own. Click the `Create` button again and you are good to go.


#### 2.2 Using the oc tool
Or run the following command from the terminal:

```
$ oc new-app -f openshift/kwek-metrics.json
```

And that's it! Now to configuring Kwek for first usage.

# 3. First configuration

#### 3.1 Get your Service Key

In order to get data from your OpenShift projects, you need an API Key. To do this, start with a dedicated project that will be used for retrieving all metrics:

```
$ oc new-project metrics-overview
```

Then, create a service account within that namespace:

```
$ oc create serviceaccount metrics-robot -n metrics-overview
```

The following one-liner looks a little beastly, but it essentially uses `oc get projects` to provide the list of all available projects, and then applies the view role to the metrics-robot for each project:

```
$ oc get projects --no-headers | while read project; do eval name=($project); oc policy add-role-to-user view system:serviceaccount:metrics-overview:metrics-robot -n ${name[0]}; done
```

The eval is unfortunately necessary to be able to only get the project name for the command.

Finally, pull the auth token out of the Service Account, and you can now use it to access all projects!

```
$ oc serviceaccounts get-token metrics-robot
```

You can confirm that the Service Account can view all projects by logging into the CLI as the Service Account:

```
$ oc login --token=`oc sa get-token metrics-robot`
$ oc projects
```

#### 3.2 Configure Kwek

The first thing you need to do is add in the ServiceAccount to the database on Kwek. You can simply access the `/services` endpoint to fill in the data.

Next, you need to add some metrics to monitor. Again, just access the `/metrics` endpoint and add the desired metrics in there.

Optionally, you can just `ssh` into your pod and run the following SQL statements inside `sqlite3`:

```
INSERT INTO `service` VALUES (1,'MyCluster','XXX','https://metrics.mycluster.openshift.com/hawkular/metrics/','https://console.mycluster.openshift.com/oapi/v1/');
INSERT INTO `metric` VALUES (1,'memory','Memory Usage','gauges/data','memory%2Fusage','MiB',9.53674e-07, 'blue');
INSERT INTO `metric` VALUES (2,'cpu','CPU Usage','gauges/data','cpu%2Fusage_rate','Millicores',1.0, 'red');
INSERT INTO `metric` VALUES (3,'network','Network Usage','gauges/data','network%2Frx_rate','KiB/s',0.0009765625, 'green');
```


# 4. Extending Kwek

The purpose of this blog post is also to show you how to quickly dive into the code and start building up on the application. If this is your case, or you simple want to play around with the code, read the sections below.

#### 4.1 Install development dependencies

In order to develop on Kwek, you need to install some extra packages:

```
$ pip install -r requirements-dev.txt
```

#### 4.2 Test the code

A good entry-point for learning how everything is glued together, is to take a look at the tests. Each python package has it's own tests, on a directory aptly named `tests/`. To run the tests, simply run the command:

```
$ py.test
```

For instance, if you are curious on how the requests to the external APIs are being processed, just dive into `api/tests/` and try to write your own test!

#### 4.3 Run in development mode

If you want to build your assets during development, it's convenient to do so with a bit more appropriate configurations. For instance, you want to be able to look at your bundle without [minification](https://github.com/JeffreyWay/laravel-mix/blob/master/docs/concatenation-and-minification.md), or with [sourcemaps](http://stackoverflow.com/questions/21719562/javascript-map-files-javascript-source-maps) to easily find out where in the code are your errors exactly.

In order to do this, you can either run the builder/bundler once, or in watch mode, so that it keeps monitoring your files and building them whenever you save some changes on them. Again, we do this by using `npm`:

```
$ npm dev
# or
$ npm watch
```



# 5. Send in your patches!

If you are extending Kwek or just totally changing it to accommodate your needs, please [let us know](https://github.com/jsvgoncalves/kwek-metrics/issues) or simply send in a [Pull Request](https://github.com/jsvgoncalves/kwek-metrics#fork-destination-box)!

If you want to collaborate but need some ideas, or if you are wondering about where to go next, here's a selection of potentially interesting features:

* It would be interesting to add e-mail notifications based on some metrics threshold.
* It would be perfect to add in asynchronous calls to get the selected metrics, something like AngularJS if you are feeling adventurous, but jQuery would also work fine.
* Customizing the charts and adding in functionalities to explore the Hawkular API would also be awesome.


So here it is how to get started displaying aggregated metrics for OpenShift using Kwek-Metrics! I hope you've enjoyed the post and see you next time.


