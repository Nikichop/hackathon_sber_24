from fastapi import FastAPI, UploadFile, File
from typing import List, Dict

app = FastAPI()


def parse_csv_with_multiple_parents(csv_content: List[str]) -> List[Dict]:
    objects = {}
    relationships = {}
    is_relationship_section = False

    for row in csv_content:
        if row.startswith('Идентификатор'):
            headers = row.strip().split(',')
            continue
        elif row.startswith('Родитель'):
            is_relationship_section = True
            continue
        elif not row.strip():
            continue
        elif not is_relationship_section:
            values = row.strip().split(',')
            object_id = int(values[0])
            objects[object_id] = dict(zip(headers, values))
            objects[object_id]['Родители'] = []
        else:
            parent_id, child_id = row.split(',')
            if int(child_id) in relationships:
                relationships[int(child_id)].append(int(parent_id))
            else:
                relationships[int(child_id)] = [int(parent_id)]

    for child_id, parents in relationships.items():
        if child_id in objects:
            objects[child_id]['Родители'].extend(parents)

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
