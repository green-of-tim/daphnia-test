import os
# from flask import Flask, request, redirect, url_for, send_from_directory
# from werkzeug.utils import secure_filename
import cv2
import numpy as np
# import matplotlib.pyplot as plt
# # import cvlib as cv
# # from cvlib.object_detection import draw_bbox
# # from numpy.lib.polynomial import poly
import math

# UPLOAD_FOLDER = 'C:/Users/Тимоша/static/images/'
# ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# app = Flask(__name__, static_url_path='/static')
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# @app.route('/', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         file = request.files['file']
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             # imgg = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename), cv2.IMREAD_GRAYSCALE)
#             img = cv2.imdecode(np.fromstring(request.files['file'].read(), np.uint8), cv2.IMREAD_UNCHANGED)
#             imgg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#             img1 = cv2.GaussianBlur(imgg, (7, 7), cv2.BORDER_DEFAULT)
#             (T, img2) = cv2.threshold(img1, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
#             kernel = np.ones((5,5),np.uint8)
#             img2 = cv2.morphologyEx(img2,cv2.MORPH_OPEN,kernel) 
#         #     img2 = cv2.GaussianBlur(img2, (7, 7), cv2.BORDER_DEFAULT)
#         #     plt.figure(figsize=(10,10))
#         #     plt.axis('off')
#         #     plt.imshow(img2)
#         #     plt.show()
#             ret, label = cv2.connectedComponents(img2)
#             res = ret

#             img2 = cv2.threshold(img1, math.floor(0.99 * T), 255, cv2.THRESH_BINARY_INV)[1]
#             ret, label = cv2.connectedComponents(img2)
#             res += ret

#             img2 = cv2.threshold(img1, math.floor(1.01 * T), 255, cv2.THRESH_BINARY_INV)[1]
#             ret, label = cv2.connectedComponents(img2)
#             res += ret

#             count = res // 3
#             # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
#             # f, axs = plt.subplots(1,2,figsize=(12,5))
#             # axs[0].imshow(img,cmap="gray")
#             # axs[1].imshow(img2,cmap="gray")
#             # axs[1].set_title("Total Daphnia Count = {}".format(res))
#             # plt.show()
#             return redirect(url_for('uploaded_file',
#                                     filename=imgg, count=count))
#     return '''
import imghdr
import os
from flask import Flask, render_template, request, redirect, url_for, abort, \
    send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config['UPLOAD_PATH'] = './static/images'

def validate_image(stream):
    header = stream.read(512)  # 512 bytes should be enough for a header check
    stream.seek(0)  # reset stream pointer
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')

@app.route('/')
def index():
    # files = os.listdir(app.config['UPLOAD_PATH'])
    # return render_template('index.html', files=files, count=request.args.get('count'))
    return render_template('index.html', count=request.args.get('count'))

@app.route('/', methods=['POST'])
def upload_files():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    count = 0
    if filename != '':
        # file_ext = os.path.splitext(filename)[1]
        # if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
        #         file_ext != validate_image(uploaded_file.stream):
        #     abort(400)
        # uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        img = cv2.imdecode(np.fromstring(request.files['file'].read(), np.uint8), cv2.IMREAD_UNCHANGED)
        imgg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        img1 = cv2.GaussianBlur(imgg, (7, 7), cv2.BORDER_DEFAULT)
        (T, img2) = cv2.threshold(img1, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
        kernel = np.ones((5,5),np.uint8)
        img2 = cv2.morphologyEx(img2,cv2.MORPH_OPEN,kernel) 
        #     img2 = cv2.GaussianBlur(img2, (7, 7), cv2.BORDER_DEFAULT)
        #     plt.figure(figsize=(10,10))
        #     plt.axis('off')
        #     plt.imshow(img2)
        #     plt.show()
        ret, label = cv2.connectedComponents(img2)
        res = ret

        img2 = cv2.threshold(img1, math.floor(0.99 * T), 255, cv2.THRESH_BINARY_INV)[1]
        ret, label = cv2.connectedComponents(img2)
        res += ret

        img2 = cv2.threshold(img1, math.floor(1.01 * T), 255, cv2.THRESH_BINARY_INV)[1]
        ret, label = cv2.connectedComponents(img2)
        res += ret

        count = res // 3
        # file_ext = os.path.splitext(filename)[1]
        # if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
        #         file_ext != validate_image(uploaded_file.stream):
        #     abort(400)
        # uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))

    return redirect(url_for('index', count=count))

@app.route('./static/images/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)
    '''
    <!doctype html>
    <html>
    <head>
        <title>File Upload</title>
    </head>
    <body>
        <h1>File Upload</h1>
        <form method="POST" action="" enctype="multipart/form-data">
        <p><input type="file" name="file"></p>
        <p><input type="submit" value="Submit"></p>
        </form>
        <hr>
        {% for file in files %}
        <img src="{{ url_for('upload', filename=file) }}" style="width: 64px">
        {% endfor %}
    </body>
    </html>
    '''
# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
    # return f"Total Daphnia count: {request.args.get('count')} <img src='C:/Users/Тимоша/static/images/{filename}'>"
