import boto3


def fetch_s3_url(prod_id):

    s3 = boto3.client('s3')
    bucket= 'refactored-image-bucket-5623'
    url = "https://refactored-image-bucket-5623.s3.eu-west-2.amazonaws.com/"
    keys = []
    path_names = []

    s3_resource = boto3.resource('s3', region_name='eu-west-2')
    s3_bucket = s3_resource.Bucket(bucket)

    fileNameSplit = prod_id.split(".") # Splits the filename to get the extension
    filename = fileNameSplit[0]

    resp = s3.list_objects_v2(Bucket=bucket)
    for obj in resp['Contents']:
        keys.append(obj['Key'])

    for key in keys:
        if filename in key:
            img = s3_bucket.Object(key)
            url_name = url + key

 return url_name

img = request.files['file'] # Takes the file, in this case apicture


def upload(prod_id, img):
    if img:
        filename = secure_filename(img.filename) # Gets the file name for the picture
        fileNameSplit = filename.split(".") # Splits the filename to get the extension
        fileExtention = fileNameSplit[1]
        if fileExtention in ALLOWED_EXTENSIONS: # Checks if the extensions are in the allowed extensions
            filename = prod_id + "." + fileExtention
            img.save(filename)
            # Uploads the file to the s3 bucket
            s3.upload_file(
                Bucket = BUCKET_NAME,
                Filename=filename,
                Key = filename
            )
            msg = "Upload Done ! " # Tells the user the upload is complete
        else:
            msg = "Not a png/jpg/jpeg." # Error occurs if the extension is not an allowed extension and tells the user this

    return