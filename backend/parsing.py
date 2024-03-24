from fastapi import FastAPI, UploadFile, File
from typing import List, Dict
from yandex_tracker_client import TrackerClient
import csv
import io
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5173",

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)
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
        if len([issue for issue in client.issues if issue.summary == task['Имя'] and issue.resolution == None]) > 0:
            continue
        if task['Команда'] not in [board.name for board in client.boards]:
            client.boards.create(name=task['Команда'], defaultQueue='GYM')
        client.issues.create(queue='Gym', summary=task['Имя'])
    
    for task in parsed_csv:
        board_id = [board.id for board in client.boards if board.name == task['Команда']][0]
        issue = [issue for issue in client.issues if issue.summary == task['Имя'] and issue.resolution == None][0]
        issue.update(boards=[{'id': board_id}])

        for rel in task['Сделать после']:
            rel_sum = [issue['Имя'] for issue in parsed_csv if int(issue['Идентификатор']) == int(rel)][0]
            rel_key = [issue.key for issue in client.issues if issue.summary == rel_sum and issue.resolution == None][0]
            issue.links.create(issue=rel_key, relationship='depends on')


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


