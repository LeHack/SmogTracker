#!/usr/bin/env python

import django, json, os, sys

# load django context and settings, so we can use gatherer below
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smogtrac.settings")
django.setup()

from optparse import OptionParser
from gatherer.service import Manager
from webui.models import Station

def main(argv=None):
    '''Command line options.'''
    program_name = os.path.basename(sys.argv[0])

    if argv is None:
        argv = sys.argv[1:]
    try:
        # setup option parser
        parser = OptionParser()
        parser.add_option("--run_by", dest="run_by", help="Internal param stating runner (defaults to Cron)")
        parser.add_option("--stations", dest="stations", help="JSON serialized list of station codes (defaults to all stations)")

        # set defaults
        parser.set_defaults(run_by=None, stations=None)

        # process options
        (opts, args) = parser.parse_args(argv)
        
        params = {}
        if opts.run_by:
            params["run_by"] = opts.run_by
        if opts.stations:
            params["stations"] = []
            for code in json.loads(opts.stations):
                 params["stations"].append(Station.objects.get(code=code))

        # run Manager
        Manager(**params).run() 

    except Exception as e:
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write("  for help use --help\n\n")
        return 2


sys.exit(main())