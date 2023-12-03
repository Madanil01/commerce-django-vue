import datetime
import os

def file_path(request, filename):
    old_filename= filename
    timeNow = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (timeNow, old_filename)
    return os.path.join('uploads/products/varian', filename)