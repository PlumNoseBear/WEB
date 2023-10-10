from flask import Flask, render_template, request, make_response, flash, redirect, send_from_directory, send_file, url_for, session
import os
from werkzeug.utils import secure_filename

from flask_uploads import UploadSet, configure_uploads, DEFAULTS

UPLOADFOLDER = 'static/files' # папка для загруженных файлов
# расширения файлов, которые можно загружать и воспроизводить
ALLOWED_EXTENSIONS = {'h5', 'pt', 'png', 'jpg', 'jpeg', 'mp4', 'mov', 'avi'}
VIDEO = {'mp4', 'mov','avi'}
VIDEOS = UploadSet('files', DEFAULTS)
VIDEOS.extensions = ('mp4', 'mov', 'avi')

# создаем экземпляр приложения
app = Flask(__name__)
# конфигурируем
app.config['UPLOADED_FILES_DEST'] = UPLOADFOLDER 
#app.config['UPLOADFOLDER'] = UPLOADFOLDER
app.secret_key = 'Scatman"s_world'
configure_uploads(app, VIDEOS)


def allowed_file(filename):
    """ Функция проверки расширения файла """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/',  methods=['GET', 'POST'])  
def upload_file():   
    if request.method == 'POST':
        # проверим, передается ли в запросе файл 
        if 'file' not in request.files:
            # После перенаправления на страницу загрузки покажем сообщение пользователю 
            flash('Не могу прочитать файл')
            return 
        file = request.files['file']
        # Если файл не выбран, то браузер может отправить пустой файл без имени.
        if file.filename == '':
            flash('Нет выбранного файла')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # безопасно извлекаем оригинальное имя файла
            filename = secure_filename(file.filename)
            flash('Сохраняю файл')
            redirect(request.url)
            # сохраняем файл
            file.save(os.path.join(app.config['UPLOADED_FILES_DEST'], file.filename))
            #return redirect(url_for('success'), file=file)
    all_files = os.listdir(app.config['UPLOADED_FILES_DEST'])
    video_files = filter(lambda x: x.split('.')[1] in VIDEO, all_files)
    dload_files = filter(lambda x: x.split('.')[1] in ALLOWED_EXTENSIONS, all_files)
    return render_template('index.html', v_files=video_files, d_files=dload_files)
    
@app.route('/download/<filename>')
def download(filename):
    # Возврат файла для скачивания
    return send_file(os.path.join(app.config['UPLOADED_FILES_DEST'], filename), as_attachment=True) 

@app.route('/play/<filename>')
def play(filename):
    return render_template('play.html', filename=filename)

@app.errorhandler(404)
def page_not(error):
    return render_template('404.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=81, debug=True)
