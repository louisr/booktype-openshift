This is a quickstart to get [Booktype][1] running at Openshift. It also create local Redis instance that required for the Booktype authoring environment to be usable. This is still a work in progress and the Redis setup definitely unsecured at this moment.

[1]:http://www.sourcefabric.org/en/booktype/

## Deployment

Run the following command, assuming you already install rhc client:-

    rhc app create -a booktype -t python-2.6
    git remote add upstream -m master git://github.com/k4ml/booktype-openshift.git
    git pull -s recursive -X theirs upstream master
    rhc app cartridge add -a booktype -c postgresql-8.4
    git push origin master

You have to create admin user manually by login to the cartridge. Use command `git remote -v` to get the cartridge id and then login using ssh.

    ssh <cartridge-id>@booktype-yournamespace.rhcloud.com
    source app-root/repo/common.env && python-2.6/virtenv/bin/django-admin.py createsuperuser

## Local Development

Assuming you use virtualenvwrapper to manage your virtualenv:-

    mkvirtualenv booktype
    python setup.py install
    source common.env && source local.env
    django-admin.py syncdb --noinput
    django-admin.py migrate
    django-admin.py loaddata documentation_licenses
    django-admin.py createsuperuser
    django-admin.py runserver

Feel free to change or remove this file, it is informational only.

## Repo layout

    wsgi/ - Externally exposed wsgi code goes
    wsgi/static/ - Public static content gets served here
    libs/ - Additional libraries
    data/ - For not-externally exposed wsgi code
    setup.py - Standard setup.py, specify deps here
    .openshift/action_hooks/pre_build - Script that gets run every git push before the build
    .openshift/action_hooks/build - Script that gets run every git push as part of the build process (on the CI system if available)
    .openshift/action_hooks/deploy - Script that gets run every git push after build but before the app is restarted
    .openshift/action_hooks/post_deploy - Script that gets run every git push after the app is restarted

## Notes about layout

Every time you push, everything in your remote repo dir gets recreated, please
store long term items (like an sqlite database) in the OpenShift data
directory, which will persist between pushes of your repo.
The OpenShift data directory is accessible relative to the remote repo
directory (../data) or via an environment variable OPENSHIFT_DATA_DIR.


## Environment Variables

OpenShift provides several environment variables to reference for ease
of use. 


When embedding a database using 'rhc app cartridge add', you can reference
environment variables for username, host and password. Example for mysql:

    os.environ['OPENSHIFT_MYSQL_DB_HOST']      - DB host
    os.environ['OPENSHIFT_MYSQL_DB_PORT']      - DB Port
    os.environ['OPENSHIFT_MYSQL_DB_USERNAME']  - DB Username
    os.environ['OPENSHIFT_MYSQL_DB_PASSWORD']  - DB Password

When embedding a NoSQL database using 'rhc app cartridge add', you can
reference environment variables for username, host and password.
Example for MongoDB:
    os.environ['OPENSHIFT_MONGODB_DB_HOST']      - NoSQL DB Host
    os.environ['OPENSHIFT_MONGODB_DB_PORT']      - NoSQL DB Port
    os.environ['OPENSHIFT_MONGODB_DB_USERNAME']  - NoSQL DB Username
    os.environ['OPENSHIFT_MONGODB_DB_PASSWORD']  - NoSQL DB Password

To get a full list of environment variables, simply add a line in your
.openshift/action_hooks/build script that says "export" and push.

## Notes about layout

Please leave wsgi, libs and data directories but feel free to create additional
directories if needed.

Note: Every time you push, everything in your remote repo dir gets recreated
please store long term items (like an sqlite database) in ../data which will
persist between pushes of your repo.

## Notes about setup.py

Adding deps to the install_requires will have the openshift server actually
install those deps at git push time.

## Reference

http://forum.sourcefabric.org/discussion/13889/deploying-to-openshift-express-wip/p1

https://github.com/razorinc/redis-openshift-example
