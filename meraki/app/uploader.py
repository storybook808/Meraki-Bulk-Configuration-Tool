from app import app
from flask import redirect, url_for, flash, request, Blueprint
from werkzeug import secure_filename


uploader_blueprint = Blueprint('uploader', __name__, template_folder='templates')


@uploader_blueprint.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    import os

    if request.method == 'POST':

        # Get the absolute path of the added file
        path = os.path.abspath(os.path.join('app', 'temp'))
        current_file = os.listdir(path)
        if len(current_file) > 0:
            # remove all files except the first
            os.remove(os.path.join(path, current_file[0]))
            print("file removed")

        # Obtain the absolute path to the file to upload using os module
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Save the uploaded file into the path specified
        # This path saves it into the current directory, then uses the join method
        # To put the file into the temp folder
        app.config['UPLOAD_FOLDER'] = os.path.join(current_dir, 'temp/')
        f = request.files['file']

        # Save the file in temp
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],
                            secure_filename(f.filename)))

        # Debug print, current_file should list all files within the temp folder
        print(current_file)

        # if there is more than a single file in the temp folder remove the extra files
        flash('file has been uploaded')

        return redirect(url_for('step2'))
