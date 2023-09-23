from flask import Flask, render_template, request, send_file
import os
import subprocess
import shutil

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'static'

# Function to clean up uploaded files and output file
def cleanup_files():
    upload_folder = os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER'])

    # Delete uploaded files
    for filename in os.listdir(upload_folder):
        file_path = os.path.join(upload_folder, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file1 = request.files['file1']
        file2 = request.files['file2']
        file3 = request.files['file3']

        if file1 and file2 and file3:
            file1.save(os.path.join(os.getcwd(),os.path.join(app.config["UPLOAD_FOLDER"], "file1.xlsx")))
            file2.save(os.path.join(os.getcwd(),os.path.join(app.config["UPLOAD_FOLDER"], "file2.xlsx")))
            file3.save(os.path.join(os.getcwd(),os.path.join(app.config["UPLOAD_FOLDER"], "file3.xlsx")))
            # Run a Python script to generate the CSV file
            script_path = os.path.join(os.getcwd(), "main.py")  # Replace with the relative path
            print(script_path)
            cmd = f'python {script_path} {os.path.join(os.getcwd(),os.path.join(app.config["UPLOAD_FOLDER"], "file1.xlsx"))} {os.path.join(os.getcwd(),os.path.join(app.config["UPLOAD_FOLDER"], "file2.xlsx"))} {os.path.join(os.getcwd(),os.path.join(app.config["UPLOAD_FOLDER"], "file3.xlsx"))} {os.path.join(os.getcwd(),os.path.join(app.config["OUTPUT_FOLDER"], "output.csv"))}'
            print(cmd)
            subprocess.run(cmd, shell=True)

            # Provide a link to download the generated CSV
            cleanup_files()  # Clean up files after processing
            return render_template('upload.html', download_link='download')

    return render_template('upload.html', download_link=None)

@app.route('/download')
def download():
    return send_file(os.path.join(os.getcwd(), 'static', 'output.csv'), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
