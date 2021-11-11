import boto3
import tempfile
import s3_bucket_operations
import bucket_names_object
import contains_all_urls_for_s3_buckets
prod_id = "aws_diagram.jpeg"
new_object = bucket_names_object.bucket_names_object()
print(new_object.getSourceBucketName)
print(new_object.getRefactoredBucketName)

# prod_id = "Baseball12"
# ext = "jpeg"

# filename = prod_id +"."+ ext

# print(filename)

# s3 = boto3.client('s3')
# """Get a list of keys in an S3 bucket."""
# bucket= 'refactored-image-bucket-5623'

# s3_2 = boto3.resource('s3', region_name='eu-west-2')
# # s3_bucket = s3.Bucket('refactored-image-bucket-5623')
# s3_bucket = s3_2.Bucket('refactored-image-bucket-5623')

# prod_id = "aws_diagram.jpeg"
# fileNameSplit = prod_id.split(".") # Splits the filename to get the extension
# filename = fileNameSplit[0]
# resp = s3.list_objects_v2(Bucket=bucket)
# for obj in resp['Contents']:
#     keys.append(obj['Key'])

# url = "https://refactored-image-bucket-5623.s3.eu-west-2.amazonaws.com/"
# path = '/home/lubuntu/Desktop/InventoryManagement/static/'

# for key in keys:
#     if filename in key:
#         img = s3.Object(key)
#         path_name = path + key
# print(path_name)




# import matplotlib.image as mpimg
# import numpy as np
# import boto3
# import tempfile

# s3 = boto3.resource('s3', region_name='us-east-2')
# bucket = s3.Bucket('bucketName')
# object = bucket.Object('dir/subdir/2015/12/7/img01.jpg')
# tmp = tempfile.NamedTemporaryFile()

# def imageSource(bucket, object, tmp):
#        with open(tmp.name, 'wb') as f:
#             object.download_fileobj(f)
#             src = tmp.name    #dir/subdir/2015/12/7/img01.jpg
#             retrun src
