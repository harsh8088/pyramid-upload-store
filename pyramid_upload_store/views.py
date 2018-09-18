from pyramid.view import view_config
from pyramid.response import Response
from PIL import Image

import os, glob
import pandas as pd
from pymongo import MongoClient

conn = MongoClient("mongodb://localhost:27017/store_db")


@view_config(route_name='home', renderer='templates/mytemplate.jinja2')
def my_view(request):
    return {'project': 'pyramid-upload-store'}


@view_config(route_name='upload',
             request_method='POST')
def upload(request):
    # Here we are just getting file into object and reading directly without store.
    # file_data = request.POST['my_file']
    # sample_data = pd.read_csv(file_data.file)
    try:
        request.storage.save(request.POST['my_file'])
        # reading uploaded csv files
        latest_files = glob.glob('/home/harsh/Dev/Samples/pyramid-upload-store/upload_dir/*')
        # reading latest uploaded csv files
        latest_file = max(latest_files, key=os.path.getctime)
        # print(latest_file)
        file_data = pd.read_csv(latest_file)
        insert_topics_collection(file_data)
        return Response("Uploaded file data processed successfully and data is stored in DB")
    except Exception as exp:
        return Response("File can't be uploaded in DB")


def insert_topics_collection(file_data):
    db = conn.store_db
    for row in range(len(file_data)):
        db.bot_topics.insert({
            "Url": file_data['Url'][row],
            "Path": file_data['Path'][row],
            "Topic": file_data['Topic'][row],
            "Contents": [file_data['Content'][row]]
        })


def resize_image(input_image_path,
                 output_image_path,
                 size):
    original_image = Image.open(input_image_path)
    width, height = original_image.size
    print('The original image size is {wide} wide x {height} '
          'high'.format(wide=width, height=height))

    resized_image = original_image.resize(size)
    width, height = resized_image.size
    print('The resized image size is {wide} wide x {height} '
          'high'.format(wide=width, height=height))
    resized_image.show()
    resized_image.save(output_image_path)


def resize_pil_image():
    size = 128, 128
    for infile in glob.glob("/home/harsh/Dev/Samples/pyramid-upload-store/upload_dir/*.jpg"):
        file, ext = os.path.splitext(infile)
        im = Image.open(infile)
        im.thumbnail(size)
        im.save(file + ".thumbnail", "JPEG")
