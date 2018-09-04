from sanic import Sanic, response
from sanic.response import json
from os.path import dirname, abspath, join

_CURDIR = dirname(abspath(__file__))

app = Sanic()
app.static('', join(_CURDIR, 'ARModels' ))

@app.route("/")
async def test(request):
    return json({"hello": "world"})

@app.route('/file')
async def handle_request(request):
    return await response.file_stream(join(_CURDIR, 'ARModels/Caramilk', 'Caramilk_revised.htm'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)