# x-api-key : token

import requests

def test_obtener_usuarios():
        #https://app.reqres.in/console
        url = "https://reqres.in/api/users?page=2"
        header = {
                "x-api-key" : "free_user_3L1hzp3PsDIicc3G8HU4BpBaO7G"
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