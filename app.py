from flask import Flask, render_template, request, redirect, url_for
from rembg import remove
from PIL import Image
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create folder if not exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['image']
        if file and file.filename:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            input_image = Image.open(filepath)
            output_image = remove(input_image)

            output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'removed_' + file.filename)
            output_image.save(output_path)

            return redirect(url_for('result', filename='removed_' + file.filename))
    return render_template('index.html')

@app.route('/result/<filename>')
def result(filename):
    return render_template('result.html', filename=filename)

if __name__ == '__main__':
    app.run(debug=True)
