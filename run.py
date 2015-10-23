#!/usr/bin/python
# Run the server

from bucketlistapp.app import create_app
import sys

modules = {
        'development': 'instance.config.DevelopmentConfig',
        'production': 'instance.config.ProductionConfig',
        'test': 'instance.config.TestingConfig',
    }

try:
    if sys.argv[1] in modules.keys():
        app = create_app(modules.get(sys.argv[1]))
        app.run(debug=app.config.get('TESTING'))
    else:
        if sys.argv[1] == '-h':
            print "python run.py <environment>"
            print "\tAvailable options:"
            print "\t - production\n\t - test\n\t - development"
        else:
            print "Invalid option passed as argument"
except IndexError:
    print "[+] python run.py -h to get help"
exit()
