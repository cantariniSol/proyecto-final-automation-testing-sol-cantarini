# x-api-key : token

import requests

def test_obtener_usuarios():
        url = "https://reqres.in/api/users/2"
        header = {
                "x-api-key" : "secrects_token"
        },
        # 1. codigo http
        response = requests.get(url,headers=header);
        codigo = response.status_code;
        assert codigo == 200;
        #print(codigo);
        data= response.json();
        #print(data);
         
        # 2. estructura

        # 3. contenido

        # 4. tiempo de respuesta 