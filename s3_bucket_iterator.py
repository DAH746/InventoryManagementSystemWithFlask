import boto3


def list_of_files(getFromSourceBucket):
    # Grabs list of all objects (names) [images in our case] from our refactored S3 bucket
    # "getFromSourceBucket" -> If true, get the items from the stock bucket, if not we would only want to get it from the refactored bucket

    if getFromSourceBucket:
        nameOfBucketToBeUsedToPullDataFrom = 'source-image-bucket-5623'
    else:
        nameOfBucketToBeUsedToPullDataFrom = 'refactored-image-bucket-5623'

        
    objectRepresentingAnS3Bucket = boto3.resource('s3')
    my_bucket = objectRepresentingAnS3Bucket.Bucket(nameOfBucketToBeUsedToPullDataFrom)
    allObjectsFromRefactoredBucket = my_bucket.objects.all()

    listOfObjectsAttainedFromGivenS3Bucket = []
    for objects in allObjectsFromRefactoredBucket:

        # # DEBUG - Following prints format of 'allObjectsFromRefactoredBucket'
        # print("Object: {}".format(allObjectsFromRefactoredBucket))

        listOfObjectsAttainedFromGivenS3Bucket.append(objects.key)
        # objects.key is the name of the file in the s3 bucket within current iteration

    print(listOfObjectsAttainedFromGivenS3Bucket)

    return listOfObjectsAttainedFromGivenS3Bucket
    # return jsonify({"listOfObjectsAttainedFromGivenS3Bucket":"{}".format(objects.key)})
