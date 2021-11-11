
# Checks if the user is logged in and therefore allowed to upload a picture to the s3 bucket
@app.route('/s3UploadTest')
def s3_upload():
    global LOGIN
    print("----------yoyoyoyo------------")
    print(LOGIN)
    
    if LOGIN: # Checks if LOGIN is true and then allows the user to upload the file
        return render_template('s3UploadTest.html')
    else:
        msg = "Please login first" # If LOGIN is false, the user is asked to login
        return render_template("result.html",msg = msg)

# # Uploads the file to the s3 bucket
# @app.route('/upload',methods=['post'])
# def upload():
#     global prod_id
#     if request.method == 'POST':
#         img = request.files['file'] # Takes the file, in this case apicture
#         if img:
#             filename = secure_filename(img.filename) # Gets the file name for the picture
#             fileNameSplit = filename.split(".") # Splits the filename to get the extension
#             fileExtention = fileNameSplit[1]
#             if fileExtention in ALLOWED_EXTENSIONS: # Checks if the extensions are in the allowed extensions
#                 filename = prod_id + "." + fileExtention
#                 img.save(filename)
#                 # Uploads the file to the s3 bucket
#                 s3.upload_file(
#                     Bucket = BUCKET_NAME,
#                     Filename=filename,
#                     Key = filename
#                 )
#                 msg = "Upload Done ! " # Tells the user the upload is complete
#             else:
#                 msg = "Not a png/jpg/jpeg." # Error occurs if the extension is not an allowed extension and tells the user this

#     return render_template("result.html",msg =msg)