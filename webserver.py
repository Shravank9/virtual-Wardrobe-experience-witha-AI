from flask import Flask, render_template, request, redirect, url_for, flash
from flask_ngrok import run_with_ngrok
from werkzeug.utils import secure_filename
from PIL import Image
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for flash messages
run_with_ngrok(app)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def main():
    return render_template('main.html')

@app.route('/fileUpload', methods=['POST'])
def file_upload():
    if 'file' not in request.files:
        flash('No file part')
        return redirect('/')
    
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect('/')
    
    if file and allowed_file(file.filename):
        filename = secure_filename('origin_web.jpg')  # Fixed filename for overwrite
        file.save(os.path.join('static', filename))
        return render_template('fileUpload.html')
    
    flash('Allowed file types are: png, jpg, jpeg')
    return redirect('/')

@app.route('/fileUpload_cloth', methods=['POST'])
def fileUpload_cloth():
    if 'file' not in request.files:
        flash('No file part')
        return redirect('/')
    
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect('/')
    
    if file and allowed_file(file.filename):
        filename = secure_filename('cloth_web.jpg')  # Fixed filename for overwrite
        file.save(os.path.join('static', filename))
        return render_template('fileUpload_cloth.html')
    
    flash('Allowed file types are: png, jpg, jpeg')
    return redirect('/')

@app.route('/view', methods=['GET'])
def view():
    print("Inference started")
    try:
        # Run inference command asynchronously if needed
        os.system("python3 main.py")
        print("Inference completed")
    except Exception as e:
        print(f"Error during inference: {str(e)}")
        flash("Error generating image")
        return redirect('/')
    
    return render_template('view.html')

if __name__ == '__main__':
    # Create static directory if not exists
    if not os.path.exists('static'):
        os.makedirs('static')
    app.run()