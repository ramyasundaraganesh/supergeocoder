from flask import Flask,render_template, request, send_file
from werkzeug.utils import secure_filename
import csv
from time import sleep
import pandas
import datetime
from geopy.geocoders import ArcGIS
import os, ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
        getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context


app=Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/success", methods=['POST'])
def success():
    global file
    if request.method=='POST':
        file=request.files['file']
        df = pandas.read_csv(file)

        headings=('ID','Name','Address','Employees','Latitude','Longitude')
        data = ()
        nom = ArcGIS()

        for row in df.itertuples():
            n = nom.geocode(row.Address)
            lat = round(n.latitude,4)
            lon = round(n.longitude,4)
            each = (row.ID, row.Name, row.Address, row.Employees, lat, lon)
            data += ((each),)
            sleep(1)

        file.save(secure_filename("uploaded"+file.filename))

        with open("uploaded"+file.filename,'w') as f:
            csv_out=csv.writer(f, delimiter=',')
            csv_out.writerow(headings)
            csv_out.writerows(data)
        return render_template("index.html",btn="download.html", headings=headings, data=data)


@app.route("/download")
def download():
    return send_file("uploaded"+file.filename,attachment_filename="yourfile.csv",as_attachment=True)

if __name__ == '__main__':
    app.debug=True
    app.run()

