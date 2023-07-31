from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np

Dados = pd.read_excel('dados.xlsx')

dados_x = Dados[['air_humidity_100', 'air_temperature_100',
       'atm_pressure_main', 'reset_norm', 'piezo_charge',
       'piezo_temperature']]


scaler1 = MinMaxScaler()

dados_x_norm = scaler1.fit_transform(dados_x)

Dados_com_chuva = dados_x[Dados.chuva != 0]
Dados_com_chuva = Dados_com_chuva[['air_humidity_100', 'air_temperature_100',
       'atm_pressure_main', 'reset_norm', 'piezo_charge',
       'piezo_temperature']]

scaler2 = MinMaxScaler()

Dados_com_chuva_norm=scaler2.fit_transform(Dados_com_chuva)



application = Flask(__name__)

# Carregar o modelo a partir do arquivo pickle
with open('classificador.pickle', 'rb') as file:
    classificador = pickle.load(file)

with open('regressao.pickle', 'rb') as file:
    regressor = pickle.load(file)




@application.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        reset_1=float(request.form['num_of_resets'])
        reset_2=float(request.form['num_of_resets_2'])
        reset_3=float(request.form['num_of_resets_3'])

        if reset_2==reset_1:
            r2=0
        else:
            r2=1

        if reset_3==reset_2:
            r3=0
        else:
            r3=1

        
        data = {
            'air_humidity_100': float(request.form['air_humidity_100']),
            'air_temperature_100': float(request.form['air_temperature_100']),
            'atm_pressure_main': float(request.form['atm_pressure_main']),
            'num_of_resets': 0,
            'piezo_charge': float(request.form['piezo_charge']),
            'piezo_temperature': float(request.form['piezo_temperature']),
            
            'air_humidity_100_2': float(request.form['air_humidity_100_2']),
            'air_temperature_100_2': float(request.form['air_temperature_100_2']),
            'atm_pressure_main_2': float(request.form['atm_pressure_main_2']),
            'num_of_resets_2': r2,
            'piezo_charge_2': float(request.form['piezo_charge_2']),
            'piezo_temperature_2': float(request.form['piezo_temperature_2']),

            'air_humidity_100_3': float(request.form['air_humidity_100_3']),
            'air_temperature_100_3': float(request.form['air_temperature_100_3']),
            'atm_pressure_main_3': float(request.form['atm_pressure_main_3']),
            'num_of_resets_3': r3,
            'piezo_charge_3': float(request.form['piezo_charge_3']),
            'piezo_temperature_3': float(request.form['piezo_temperature_3'])
        }

        dados = np.array(list(data.values()))
        print(len(dados))
        dados_norm = scaler1.transform(dados.reshape(3,6))
        print(dados_norm)
        prev = classificador.predict(dados_norm.reshape(1,18))

        print(prev)

        if prev[0] ==1:
            
            
            return jsonify({"Resultado":"Chuva Prevista:" + str(regressor.predict(dados_norm.reshape(1,18)))})
        else:

            return jsonify({"Resultado":"Nao Choveu!"})


    
    return render_template('formulario.html')


    

# Executar a API
if __name__ == '__main__':
    application.run()
