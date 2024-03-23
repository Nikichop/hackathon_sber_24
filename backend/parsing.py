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
    headers = next(reader)

    for values in reader:
        if not values:
            continue
        object_id = int(values[0])
        objects[object_id] = dict(zip(headers, values))
        after_field = values[-1]
        if after_field:
            objects[object_id]['Сделать после'] = list(map(int, after_field.split(',')))
        else:
            objects[object_id]['Сделать после'] = []

    return list(objects.values())

def put_data_to_tracker(parsed_csv: dict):
    for task in parsed_csv:
        if len(client.issues.find(f'Summary: "{task['Имя']}" Resolution: empty() Queue: "GYM"')) > 0:
            issues = client.issues.find(f'Summary: "{task['Имя']}" Resolution: empty() Queue: "GYM"')
            continue

        issue = client.issues.create(queue='Gym', summary=task['Имя'])
        if task['Команда'] not in [board.name for board in client.boards]:
            client.boards.create(name=task['Команда'], defaultQueue='GYM')

        board_id = 1
        for board in client.boards:
            if board.name == task['Команда']:
                board_id = board.id
        issue.update(boards=[{'id': board_id}])


@app.post("/upload/")
async def upload_csv(file: UploadFile = File(...)):
    if file.content_type == 'text/csv':
        try:
            csv_content = (await file.read()).decode('utf-8')
            data = parse_csv_with_multiple_parents(csv_content)
            put_data_to_tracker(data)
            return {'data': data}
        except Exception as e:
            return {"error": f"Error processing CSV file: {str(e)}"}
    else:
        return {"error": "Incorrect file format. Please upload a CSV file."}
