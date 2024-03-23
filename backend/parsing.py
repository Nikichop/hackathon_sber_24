from fastapi import FastAPI, UploadFile, File
from typing import List, Dict
from yandex_tracker_client import TrackerClient
import csv
import io

app = FastAPI()
client = TrackerClient(token="y0_AgAAAAAUf2HOAAt_cgAAAAD_OQTuAAA-mPvZ6hpEjq9TA0T0yC30vzNXSQ", cloud_org_id="bpfud6rvc4vqm8f4qpu6")

def parse_csv_with_multiple_parents(csv_content: str) -> List[Dict]:
    objects = {}
    reader = csv.reader(io.StringIO(csv_content), delimiter=',', quotechar='"')
    headers = next(reader)  # Пропускаем заголовки

    for values in reader:
        if not values:  # Пропускаем пустые строки
            continue
        object_id = int(values[0])
        objects[object_id] = dict(zip(headers, values))
        # Обработка поля "Сделать после"
        after_field = values[-1]
        if after_field:
            objects[object_id]['Сделать после'] = list(map(int, after_field.split(',')))
        else:
            objects[object_id]['Сделать после'] = []

    return list(objects.values())


@app.post("/upload/")
async def upload_csv(file: UploadFile = File(...)):
    filename = file.filename
    if filename.endswith('.csv'):
        try:
            csv_content = (await file.read()).decode('utf-8')
            data = parse_csv_with_multiple_parents(csv_content)
            for task in data:
                if len(client.issues.find(f'Summary: "{task['Имя']}" Resolution: empty() Queue: "GYM"')) > 0:
                    continue
                issue = client.issues.create(queue='Gym', summary=task['Имя'])
            return {"data": data}
        except Exception as e:
            return {"error": f"Error processing CSV file: {str(e)}"}
    else:
        return {"error": "Only CSV files are allowed."}
