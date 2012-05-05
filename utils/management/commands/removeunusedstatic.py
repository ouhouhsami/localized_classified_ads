import os
import re

from django.core.management.base import NoArgsCommand
from django.conf import settings
from django.contrib.staticfiles import finders
from django.utils.datastructures import SortedDict


class Command(NoArgsCommand):
    """
    Command that remove unused static files
    """
    help = "Remove unused static files."
    def handle_noargs(self, **options):
        found_files = SortedDict()
        for finder in finders.get_finders():
            for path, storage in finder.list(['CVS', '.*', '*~']):
                # Prefix the relative path if the source storage contains it
                if getattr(storage, 'prefix', None):
                    prefixed_path = os.path.join(storage.prefix, path)
                else:
                    prefixed_path = path

                if prefixed_path not in found_files:
                    found_files[prefixed_path] = (storage, path)

        for app in settings.INSTALLED_APPS:
            app = __import__(app)
            path =  app.__path__[0]

# il faut parser aussi les templates, 

            for root, sub_folders, files in os.walk(path):
                for file in files:
                    if not re.search("(\.DS_Store|\.ttf$|\.pyc$)", file):
                        #file_list.append(os.path.join(root, file))
                        path = os.path.join(root, file)
                        f = open(path)
                        try:
                            #print 'good'
                            for line in f:
                                for static_file in found_files:
                                    if static_file in line:
                                    #static_media_list.remove(static_file)
                                        print 'there', static_file, path, line
                        except:
                            #print 'bad', path
                            pass