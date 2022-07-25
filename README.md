# fiuba-fallas

TP final de Sistemas Expertos para Fallas I

## Backend

```bash
cd back
pip install -r requirements.txt
python3 app.py
```

Ejemplo de API JSON:
```json
-- POST http://127.0.0.1:5000/analisis
c/ body:
{
    "hisopado": "POSITIVO",
    "sintomasPaciente": 2,
    "estadoClinico": "ESTABLE"
}

response:
{
    "sugerencias_contactos_estrechos": [
        "Indicar aislamiento"
    ],
    "sugerencias_paciente": [
        "Indicar aislamiento",
        "Tratar con medicamentos",
        "Llamar periodicamente, cada 10 dias"
    ]
}
```

## Frontend

```bash
cd app
npm install
npm run start
```
