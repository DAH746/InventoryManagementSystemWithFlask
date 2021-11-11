import boto3
import tempfile
import s3_bucket_operations
import bucket_names_object
import contains_all_urls_for_s3_buckets
prod_id = "aws_diagram.jpeg"
new_object = bucket_names_object.bucket_names_object()
print(new_object.getSourceBucketName)
print(new_object.getRefactoredBucketName)

prod_id = "12312313"
ext = "jpg"

temp_url = s3_bucket_operations.getURLOfONEObjectWithinAnS3Bucket(new_object.getRefactoredBucketName, prod_id)
print(temp_url)
filename = prod_id +"."+ ext

print(filename)

s3 = boto3.client('s3')

# def getUrlForOneProd(prod_id):
#     """Get a list of keys in an S3 bucket."""
#     keys = []
#     s3_resource = boto3.resource('s3')
#     s3_bucket = s3_resource.Bucket(new_object.getRefactoredBucketName)

#     fileNameSplit = prod_id.split(".") # Splits the filename to get the extension
#     filename = fileNameSplit[0]
#     filename = filename + "_"

#     resp = s3.list_objects_v2(Bucket=new_object.getRefactoredBucketName)
#     for obj in resp['Contents']:
#         keys.append(obj['Key'])

#     for key in keys:
#         if filename in key:
#             path_name = s3_bucket_operations.getURLOfONEObjectWithinAnS3Bucket(new_object.getRefactoredBucketName, key)
#     return path_name

path = s3_bucket_operations.getUrlForOneProd(prod_id)
print(path)
