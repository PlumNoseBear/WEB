from flask import Flask, render_template, request, make_response, flash, redirect, send_from_directory, url_for, session
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/files' # папка для загруженных файлов
# расширения файлов, которые можно загружать
ALLOWED_EXTENSIONS = {'h5', 'pt', 'png', 'jpg', 'jpeg', 'mp4', 'avi'}
# создаем экземпляр приложения
app = Flask(__name__)
# конфигурируем
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'Scatman"s_world'

def allowed_file(filename):
    """ Функция проверки расширения файла """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/',  methods=['GET', 'POST'])
def index():
    play_files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', files=play_files)

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
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            return redirect(url_for('/success'))
    
    return render_template('index.html')
  
def download_file():
  ...

@app.route('/success', methods = ['POST']) 
def success(): 
    if request.method == 'POST': 
        f = request.files['file'] 
        f.save(file.filename)
        flash(f"Загружен файл {filename}")
    return render_template("index.html")

@app.route('/play/<filename>')
def play(filename):
    return render_template('play.html', filename=filename)

@app.errorhandler(404)
def page_not(error):
    return render_template('404.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=81, debug=True)
