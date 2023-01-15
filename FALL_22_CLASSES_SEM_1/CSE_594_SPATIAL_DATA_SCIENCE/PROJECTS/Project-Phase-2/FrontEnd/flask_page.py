# ===== IMPORTS ===========
import os
from pathlib import Path
from flask import Flask, render_template, request, redirect, flash
from constants import *
from flask_controller import *

# ========== VARIABLES ==============
app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = os.path.join(Path.cwd(), 'uploads')
app.config['INTERMEDIATE_FOLDER'] = os.path.join(Path.cwd(), 'intermediate')
OUTPUT_FILE_NAME = 'data.json'


# =========== ROUTES ==================

# ====== RENDER HOME PAGE ======
@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    return render_template('html/homeNew.html')


# ====== RENDER ABOUT PAGE
@app.route("/about", methods=['GET', 'POST'])
def about():
    return render_template('html/about.html')


# ====== RENDER UPLOAD FILE PAGE ======
@app.route("/uploadDataset", methods=['GET', 'POST'])
def dataset():
    if request.method == 'GET':
        return render_template('html/uploadFile.html')

    if request.method == 'POST':

        # CHECK IF FILE IS PRESENT IN THE REQUEST BODY
        if 'path' not in request.files:
            flash('No file part')
            return redirect(request.url)

        # GET FILE NAME
        file = request.files['path']

        # SEE IF FILE NAME IS VALID
        if file.filename != '' and allowed_file(file.filename):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            # GET RESPONSE FROM BACKEND TO SEE IF FILE GLOBAL VARIABLE WAS UPDATED AT BACKEND
            # loadDF = getLoadedDataFrame2(loadURL, file_path)
            # print(loadDF)
            writeToFile(load_dataset(file_path),os.path.join(app.config['INTERMEDIATE_FOLDER'], OUTPUT_FILE_NAME))
            return redirect('/')
        return render_template('html/uploadFile.html')


# ====== RENDER SPATIAL RANGE PAGE ======
@app.route("/spatialRange", methods=['GET', 'POST'])
def spatialRange():
    if request.method == 'GET':
        return render_template('html/spatial_range.html')

    if request.method == 'POST':
        latMin = float(request.form.get("latmin"))
        lonMin = float(request.form.get("lonmin"))
        latMax = float(request.form.get("latmax"))
        lonMax = float(request.form.get("lonmax"))

        # GET DATAFRAME AND JSON PAYLOAD
        # DF - TO RENDER ON HTML AS TABLE
        # JSON - TO SAVE IT TO FILE TO LATER DISPLAY ON TRIPS LAYER
        dfGSR, dataJson = getGSRDataFrame(gsrURL, latMin, lonMin, latMax, lonMax)
        dataJson = updateJson(dataJson)
        writeToFile(dataJson, os.path.join(app.config['INTERMEDIATE_FOLDER'], OUTPUT_FILE_NAME))
        return render_template('html/htmlOutputs/output.html', tables=[dfGSR.to_html(classes='data', header="true")])


# ====== RENDER SPATIAL TEMPORAL RANGE PAGE ======
@app.route("/spatialTemporalRange", methods=['GET', 'POST'])
def spatialTemporalRange():
    if request.method == 'GET':
        return render_template('html/spatial_temporal_range.html')

    if request.method == 'POST':
        timemin = int(request.form.get("timemin"))
        timeMax = int(request.form.get("timemax"))
        latMin = float(request.form.get("latmin"))
        lonMin = float(request.form.get("lonmin"))
        latMax = float(request.form.get("latmax"))
        lonMax = float(request.form.get("lonmax"))

        # GET DATAFRAME AND JSON PAYLOAD
        # DF - TO RENDER ON HTML AS TABLE
        # JSON - TO SAVE IT TO FILE TO LATER DISPLAY ON TRIPS LAYER
        dfGSTR, dataJson = getGSTRDataFrame(gstrURL, timemin, timeMax, latMin, lonMin, latMax, lonMax)
        dataJson = updateJson(dataJson)
        writeToFile(dataJson, os.path.join(app.config['INTERMEDIATE_FOLDER'], OUTPUT_FILE_NAME))
        return render_template('html/htmlOutputs/output.html', tables=[dfGSTR.to_html(classes='data', header="true")])


# ====== RENDER KNN PAGE ======
@app.route("/knn", methods=['GET', 'POST'])
def knn():
    if request.method == 'GET':
        return render_template('html/knn.html')

    if request.method == 'POST':
        trajectoryId = int(request.form.get("trajectoryId"))
        k = int(request.form.get("value-k"))

        # GET DATAFRAME PAYLOAD
        # DF - TO RENDER ON HTML AS TABLE
        GKnnResult = getKNNDataFrame(gKnnURL, trajectoryId, k)
        return render_template('html/htmlOutputs/output.html',
                               tables=[GKnnResult.to_html(classes='table table-stripped', header="true")])


# ====== RENDER TRIPS LAYER PAGE ======
@app.route("/renderTrips", methods=['GET', 'POST'])
def render():
    f = open(os.path.join(app.config['INTERMEDIATE_FOLDER'], OUTPUT_FILE_NAME))
    data = json.load(f)
    viewState = getViewState(data)
    f.close()
    return render_template('html/trips_layer.html', data=data, vs=viewState)


if __name__ == '__main__':
    app.run(debug=True)
