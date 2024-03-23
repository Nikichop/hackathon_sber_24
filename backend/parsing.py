from fastapi import FastAPI, UploadFile, File
from typing import List, Dict
import csv
import io

app = FastAPI()


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


@app.post("/upload/")
async def upload_csv(file: UploadFile = File(...)):
    if file.content_type == 'text/csv':
        try:
            csv_content = (await file.read()).decode('utf-8')
            data = parse_csv_with_multiple_parents(csv_content)
            return {"data": data}
        except Exception as e:
            return {"error": f"Error processing CSV file: {str(e)}"}
    else:
        return {"error": "Incorrect file format. Please upload a CSV file."}
