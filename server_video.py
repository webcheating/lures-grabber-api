from flask import Flask, render_template, request, jsonify
import os
import base64

app = Flask(__name__)


if not os.path.exists('uploads'):
    os.makedirs('uploads')

#@app.route('/upload', methods=['POST'])
#def upload_image():
#    data = request.json['image']
#    image_data = base64.b64decode(data.split(',')[1]) 
#
#    # Сохраняем изображение на диск
#    with open(os.path.join('uploads', 'image.png'), 'wb') as f:
#        f.write(image_data)
#
#    return 'Image received', 200


def get_next_png_filename(directory, extension='.png'):
    
    files = [f for f in os.listdir(directory) if f.endswith(extension)]

    if not files:
        return '1' + extension

    numbers = [int(os.path.splitext(f)[0]) for f in files]
    next_number = max(numbers) + 1  # next number
    return f'{next_number}{extension}'

def get_next_webm_filename(directory, extension='.webm'):
    files = [f for f in os.listdir(directory) if f.endswith(extension)]

    if not files:
        return '1' + extension

    numbers = [int(os.path.splitext(f)[0]) for f in files]
    next_number = max(numbers) + 1 
    return f'{next_number}{extension}'


@app.route('/upload', methods=['POST'])
def upload_file():
    # file check
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    # file type check
    if file.mimetype not in ['image/png', 'video/webm']:
        return jsonify({'error': 'Invalid file type'}), 400

    # change filename
    filename_png = get_next_png_filename('uploads')
    filename_webm = get_next_webm_filename('uploads')
    
    # change filename
    if file.mimetype == 'image/png':
        filename = get_next_png_filename('uploads')
    elif file.mimetype == 'video/webm':
        filename = get_next_webm_filename('uploads')

    # save file
    file_path = os.path.join('uploads', filename)
    file.save(file_path)

    return jsonify({'message': 'File successfully uploaded', 'path': file_path}), 200


#@app.route('/upload', methods=['POST'])
#def upload_image():
#    # file check
#    if 'file' not in request.files:
#        return jsonify({'error': 'No file part'}), 400
#
#    file = request.files['file']
#
#    # file type check
#    if file.mimetype != 'image/png':
#        return jsonify({'error': 'Invalid file type'}), 400
#
#    filename = get_next_filename('uploads')
#
#    # save file
#    file_path = os.path.join('uploads', filename)
#    file.save(file_path)
#
#    return jsonify({'message': 'File successfully uploaded', 'path': file_path}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, ssl_context=('/etc/letsencrypt/live/webcheating.cc/fullchain.pem', '/etc/letsencrypt/live/webcheating.cc/privkey.pem'))

