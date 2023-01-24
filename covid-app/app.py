from flask import Flask,render_template, request
from itertools import groupby
from operator import itemgetter
import requests

#inisialisasi object flask
app = Flask(__name__)


# fungsi untuk get data api
def get_data_api(url):
    data = ''
    url = url
    data =requests.get(url).json()
    return data


@app.route('/')
def index():
    data =  get_data_api('https://dekontaminasi.com/api/id/covid19/stats')
    return  render_template('index.html', data = data)

@app.route('/hospital', methods=['GET','POST'])
def show_hospital():

    if request.method == 'POST':
       ## sorting data use with sorted() & lambda
       data = get_data_api('https://dekontaminasi.com/api/id/covid19/hospitals')
       data = sorted(data, key=lambda k: k[request.form['filter']])
    else:
       data = get_data_api('https://dekontaminasi.com/api/id/covid19/hospitals')

    return render_template('hospitals.html', data = data)

@app.route('/detail_hospital/<province>')
def detail_hospital(province):

    data = get_data_api('https://dekontaminasi.com/api/id/covid19/hospitals')
    # pake filter buat ngefilter data yang sesuai sama parameter
    filtered = filter(lambda d:d['province'] == province, data)
    list_kota = []
    filtered = sorted(filtered, key = itemgetter('province'))
    for key, value in groupby (filtered, key = itemgetter('region')):
        list_kota.append(key)


    return render_template('detail_hospital.html', data = filtered , province = province ,list_kota =list_kota)

@app.route('/news')
def show_news():

    data = get_data_api('https://dekontaminasi.com/api/id/covid19/news')
    print(data)
    return render_template('news.html', data=data)
# Buat ngedebug -> jadi kalo save file ga perlu jalanin flask run terus
if __name__ == "__main__":
    app.run(debug=True)
