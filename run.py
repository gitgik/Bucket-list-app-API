import sys
from bucket.app import create_app

environments = {
    'test': 'instance.config.TestingConfig',
    'development': 'instance.config.DevelopmentConfig',
    'production': 'instance.config.ProductionConfig'
}

try:
    if sys.argv[1] in environments.keys():
        app = create_app(environments.get(sys.argv[1]))
        # Run the app
        app.run(debug=app.config.get('TESTING'))
    else:
        if sys.argv[1] == '-h' or sys.argv[1] == '--help':
            print ('Usage: python run.py <environment>')
            print ('\n Available options')
            print ('\t -- production \n\t -- development \n\t -- test')
except IndexError:
    # Handle missing arguments or more unfriendly options than required
    print ("Missing options: use [python run.py -h] \
         to get list of available options")
exit()
