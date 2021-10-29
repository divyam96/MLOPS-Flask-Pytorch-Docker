from flask import Flask, render_template, request, redirect, url_for
from models import MobileNet
import os
from math import floor

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static'

model = MobileNet()
display_images = [os.path.join(app.config['UPLOAD_FOLDER'], 'sample_image.jpg')]

@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/infer', methods=['POST'])
@app.route('/')
def success():
    if request.method == 'POST':
        uploaded_files = request.files.getlist("files[]")
        for i, f in enumerate(uploaded_files):
            if i == 3:
                break
            saveLocation = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
            f.save(saveLocation)
            if len(display_images) == 5:
                extra_file = display_images.pop(0)
                display_images.append(saveLocation)
                if 'sample_image.jpg' not in extra_file:
                    os.remove(extra_file)
            else:
                display_images.append(saveLocation)

    result_tuple_list = []
    # saveLocation = f.filename
    for image_path in display_images:
        inference, confidence = model.infer(image_path)  # image_path, 0.9
        confidence = floor(confidence * 10000) / 100
        result_tuple_list.append((inference, confidence,  os.path.split(image_path)[-1]))

    # delete file after making an inference
    # respond with the inference
    return render_template('inference.html', results=result_tuple_list)


if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 80))
    app.run(host='0.0.0.0', port=port, debug=True)
