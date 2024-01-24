from flask import Flask, send_file, render_template, request
from detect_objects import get_live_image, detect_objects
from threading import Thread
from data import read_data


app = Flask(__name__)

detection = Thread(target=detect_objects)

def index():
    data = read_data(file='data.json')
    cars = data['cars']
    avg = data['avg']
    if request.method == 'GET':
        return render_template('index.html', cars=cars, avg=avg)
    elif request.method == 'POST':
        return send_file('live.jpg', mimetype='image/jpeg', cars=cars, avg=avg)
    
def test():
    if request.method == 'GET':
        return render_template('test.html')
    elif request.method == 'POST':
        image = request.files['image']
        image = get_live_image('../static/detection.jpg')
        return send_file('detection.jpg', mimetype='image/jpeg')
    

@app.route('/', methods=['GET', 'POST'])
def main():
    return index()

@app.route('/test', methods=['GET', 'POST'])
def main_test():
    return test()

if __name__ == '__main__':
    app.run()