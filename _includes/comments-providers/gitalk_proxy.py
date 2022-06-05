import requests
import flask
from flask_cors import CORS

server = flask.Flask(__name__)

# 跨域访问问题
CORS(server, resources=r'/*')

# github auth
client_id = "b5ad6687bca9e719250d"
client_secret = "03676b4cbb88ab5b7acf245927104406e1767435"


# 接口返回格式 {"access_token":"gho_COSr3lUITUX9b2J7krsKjNlnlNSOBw2g0oZ1","token_type":"bearer","scope":"public_repo"}
@server.post('/get_access_token')
def get_access_token():
    url = 'https://github.com/login/oauth/access_token'
    params = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': flask.request.json['code']
    }
    headers = {
        'accept': 'application/json'
    }
    result = requests.post(url=url, params=params, headers=headers, verify=False)
    # 存储access_token
    # ..暂时不需要
    return result.json()


if __name__ == '__main__':
    server.run(host='127.0.0.2', port=8011, debug=False)
