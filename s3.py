import boto
import boto.s3
import os.path
import sys
import time
import datetime
# Fill these in - you get them when you sign up for S3
AWS_ACCESS_KEY_ID = 'xxxxxxxxxxxx'
AWS_ACCESS_KEY_SECRET = 'xxxxxxxxxxxxxxxxxxxxxxx'
# Fill in info on data to upload
# destination bucket name
bucket_name = 'bucket-name'
# source directory
sourceDir = '/var/www/html/wordpress'
# destination directory name (on s3)
utc_timestamp = time.time()
UTC_FORMAT = '%Y%m%d'
utc_time = datetime.datetime.utcfromtimestamp(utc_timestamp)
utc_time = utc_time.strftime(UTC_FORMAT)
print (utc_time)
destDir = ''
#max size in bytes before uploading in parts. between 1 and 5 GB recommended
MAX_SIZE = 20 * 1000 * 1000
#size of parts when uploading in parts
PART_SIZE = 6 * 1000 * 1000
conn = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_ACCESS_KEY_SECRET)
bucket = conn.get_bucket(bucket_name)
uploadFileNames = []
for root, dirs, files in os.walk(sourceDir, topdown=False):
       for name in files:
          fname=os.path.join(root, name)
          print (fname)
          uploadFileNames.append(fname)
          print (uploadFileNames)
def percent_cb(complete, total):
    sys.stdout.write('.')
    sys.stdout.flush()
for filenames in uploadFileNames:
        filename=filenames.replace("\\", "/")
        print ('filename=' + filename)
        sourcepath = filename
        destpath = utc_time + '/' + filename
        #print ('Uploading %s to Amazon S3 bucket %s') % \
               #(sourcepath, bucket_name)
        filesize = os.path.getsize(sourcepath)
        if filesize > MAX_SIZE:
            print ("multipart upload")
            mp = bucket.initiate_multipart_upload(destpath)
            fp = open(sourcepath,'rb')
            fp_num = 0
            while (fp.tell() < filesize):
                fp_num += 1
                print ("uploading part %i" %fp_num)
                mp.upload_part_from_file(fp, fp_num, cb=percent_cb, num_cb=10, size=PART_SIZE)
            mp.complete_upload()
        else:
            print ("singlepart upload")
            k = boto.s3.key.Key(bucket)
            k.key = destpath
            k.set_contents_from_filename(sourcepath,
                    cb=percent_cb, num_cb=10)
