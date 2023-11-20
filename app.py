from flask import Flask, render_template, request, send_from_directory, session, redirect, url_for
import os
from flask import jsonify

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

@app.route('/')
def index():
    # List directories in 'Photos'
    folder_path = os.path.join(app.root_path, 'static/photos')
    folders = [name for name in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, name))]
    return render_template('index.html', folders=folders, completed_folders=session.get('completed_folders'))

@app.route('/delete-images', methods=['POST'])
def delete_images():
    data = request.get_json()
    image_paths = [os.path.join(app.root_path, 'static', image) for image in data['images']]
    for image_path in image_paths:
        try:
            os.remove(image_path)
        except OSError as e:
            print(f"Error deleting image {image_path}: {e.strerror}")
            return jsonify({"error": e.strerror}), 500
    return jsonify({"success": True}), 200

@app.route('/toggle_done/<folder_name>', methods=['POST'])
def toggle_done(folder_name):
    # Get the list of completed folders from the session
    completed_folders = session.get('completed_folders', [])
    # Toggle the folder's state
    if folder_name in completed_folders:
        completed_folders.remove(folder_name)  # Mark as not done
    else:
        completed_folders.append(folder_name)  # Mark as done
    # Update the session
    session['completed_folders'] = completed_folders

    # Redirect to the images page for the current folder
    return redirect(url_for('show_images', folder_name=folder_name))

@app.route('/folder/<folder_name>')
def show_images(folder_name):
    image_folder = 'Photos/' + folder_name  # Use a forward slash
    full_folder_path = os.path.join(app.root_path, 'static', image_folder.replace('\\', '/'))  # Replace backslashes
    images = [os.path.join(image_folder.replace('\\', '/'), file).replace('\\', '/') for file in os.listdir(full_folder_path) if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    return render_template('images.html', images=images, folder_name=folder_name, completed_folders=session.get('completed_folders'))

if __name__ == '__main__':
    app.run(debug=True)
