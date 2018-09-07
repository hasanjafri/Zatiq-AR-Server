from sanic import Sanic, response
from sanic.response import json
from os.path import dirname, abspath, join
from ar_model_client import ZatiqARModelClient

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

@app.route('/upload/', methods=['POST'])
async def upload_ar_model(request):
    if 'ar_model_zip' not in request.files:
        return response.json({'message': "Error! No AR Model zip was uploaded!"})
    else:
        ar_model_zip = request.files['ar_model_zip']
        return await zatiq_ar_model_client.save_ar_model_locally(ar_model_zip)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
