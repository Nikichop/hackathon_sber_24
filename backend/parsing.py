from fastapi import FastAPI, UploadFile, File
from typing import List, Dict

app = FastAPI()


def parse_csv_with_multiple_parents(csv_content: List[str]) -> List[Dict]:
    objects = {}
    for row in csv_content:
        if row.startswith('Идентификатор'):
            headers = row.strip().split(',')
            continue
        elif not row.strip():
            continue
        else:
            values = row.strip().split(',')
            object_id = int(values[0])
            objects[object_id] = dict(zip(headers, values))
            if values[-1]:
                objects[object_id]['Сделать после'] = list(map(int, values[-1].strip('"').split(',')))
            else:
                objects[object_id]['Сделать после'] = []

    return list(objects.values())


@app.post("/upload/")
async def upload_csv(file: UploadFile = File(...)):
    filename = file.filename
    if filename.endswith('.csv'):
        try:
            csv_content = (await file.read()).decode('utf-8').split('\n')
            data = parse_csv_with_multiple_parents(csv_content)
            return {"data": data}
        except Exception as e:
            return {"error": f"Error processing CSV file: {str(e)}"}
    else:
        return {"error": "Only CSV files are allowed."}
