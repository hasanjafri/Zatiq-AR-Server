from sanic import Sanic, response
from sanic.response import json
from os.path import dirname, abspath, join
from ar_model_client import ZatiqARModelClient
from config import admin_password, admin_username

_CURDIR = dirname(abspath(__file__))
zatiq_ar_model_client = ZatiqARModelClient()

app = Sanic()
app.static('', join(_CURDIR, 'ARModels' ))

@app.route("/")
async def test(request):
    return json({"hello": "world"})

@app.route('/Model/<folder>/<index__file>')
async def handle_request(request):
    return await response.file_stream(join(_CURDIR, 'ARModels/'+str(folder), index_file))

ALLOWED_EXTENSIONS = set(['zip'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload/', methods=['POST'])
async def upload_ar_model(request):
    if 'file' not in request.files:
        return response.json({'message': "Error! No AR Model zip was uploaded!"}, 400)
    if 'username' not in request.form:
        return response.json({'message': "Error! Please enter the admin username!"}, 400)
    if 'password' not in request.form:
        return response.json({'message': "Error! Please enter the admin password!"}, 400)

    username = request.form.get('username')
    password = request.form.get('password')

    zip_files = request.files['file'].read()

    if username == admin_username and password == admin_password:
        return await zatiq_ar_model_client.save_ar_model_locally(zip_files)
    else:
        return response.json({'message': 'Error! Invalid admin credentials!'})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
