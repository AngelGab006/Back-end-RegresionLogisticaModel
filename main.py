import joblib
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS

try:
    model_pipeline = joblib.load('modelo_regresion_logistica.pkl')
    print("Modelo cargado exitosamente.")
except FileNotFoundError:
    print("ERROR: Asegúrate de que 'modelo_regresion_logistica.pkl' esté en este directorio.")
    model_pipeline = None

app = Flask(__name__)
CORS(app) 

COLUMNS = [
    'edad', 'genero', 'altura', 'peso', 'presion_sistolica', 
    'presion_diastolica', 'colesterol', 'glucosa', 'fuma', 'bebe', 'actividad'
]

@app.route('/predict', methods=['POST'])
def predict():
    if model_pipeline is None:
        return jsonify({'error': 'Modelo no disponible'}), 500

    try:
        data = request.get_json(force=True)
        
        df_new = pd.DataFrame([data], columns=COLUMNS)

        for col in df_new.columns:
            df_new[col] = pd.to_numeric(df_new[col], errors='coerce') 
        
        if df_new.isnull().values.any():
            return jsonify({'error': 'Datos de entrada incompletos o inválidos.'}), 400

        prediction = model_pipeline.predict(df_new)[0]
        
        probability_of_risk = model_pipeline.predict_proba(df_new)[0][1] * 100
        
        return jsonify({
            'cardio_risk': int(prediction), 
            'risk_percentage': f'{probability_of_risk:.2f}'
        })

    except Exception as e:
        print(f"ERROR CRÍTICO EN LA PREDICCIÓN: {e}")
        return jsonify({'error': f'Error interno del servidor. Detalle: {e}'}), 500

if __name__ == '__main__':
    app.run(debug=True)