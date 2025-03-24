def index():
    if request.method == 'POST':
        image_data = request.form.get('signature')
        if not image_data:
            return "No signature provided!", 400
        image_data = image_data.split(',')[1]
        if pred(base64.b64decode(image_data), model_path='/app/model_AlexNet.pth'):