from fastapi import FastAPI, UploadFile, File
from typing import List, Dict
from yandex_tracker_client import TrackerClient
import csv
import io
from starlette.middleware.cors import CORSMiddleware
from datetime import datetime
from collections import defaultdict
from math import exp


from operations.mail_router import router as mail

app = FastAPI()

origins = [
    "http://localhost:5173",
]
app.include_router(mail)
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
        if len([issue for issue in client.issues if issue.summary == task['Имя'] and issue.resolution == None and issue.queue.key == "GYM"]) > 0:
            continue

        if task['Команда'] not in [board.name for board in client.boards]:
            client.boards.create(name=task['Команда'], defaultQueue='GYM')
        client.issues.create(queue='Gym', summary=task['Имя'], storyPoints=task['Трудозатраты'], start=task['Дата начала'], deadline=task['Дедлайн'])
    
    for task in parsed_csv:
        board_id = [board.id for board in client.boards if board.name == task['Команда']][0]
        issue = [issue for issue in client.issues if issue.summary == task['Имя'] and issue.resolution == None and issue.queue.key == "GYM"][0]
        issue.update(boards=[{'id': board_id}])

        for rel in task['Сделать после']:
            rel_sum = [issue['Имя'] for issue in parsed_csv if int(issue['Идентификатор']) == int(rel)][0]
            rel_key = [issue.key for issue in client.issues if issue.summary == rel_sum and issue.resolution == None and issue.queue.key == "GYM"][0]
            try:
                issue.links.create(issue=rel_key, relationship='depends on')
            except Exception as e:
                if e.args[0].status_code != 422:
                    raise e

def calc_progress(start, end, status_key) -> float:
    startDate = None
    if start != None:
        startDate = datetime(int(start[:4]), int(start[5:7]), int(start[8:10]), 10, 0)

    endDate = None
    if end != None:
        endDate = datetime(int(end[:4]), int(end[5:7]), int(end[8:10]), 10, 0)

    currentDate = datetime.now()

    progress = 0
    if startDate != None or endDate != None:
        currDiff = (currentDate - startDate)
        currDiff = currDiff.days * 24 * 60 * 60 + currDiff.seconds
        expDiff = (endDate - startDate)
        expDiff = expDiff.days * 24 * 60 * 60 + expDiff.seconds
        if currDiff >= 0 and expDiff != 0:
            progress = (currDiff / expDiff) * 100
    if status_key == 'closed':
        progress = 100

    return progress

def get_depends_tasks(issue) -> list:
    res = []

    for link in issue.links:
        if link.direction == 'outward' and link.type.id == 'depends':
            res.append(link.object.key)

    return res

def filter_for_level(data, group = 'Любой'):
    res = []
    nodes = {item['key']: item for item in data}
    levels = defaultdict(list)

    def compute_level(node_id):
        if node_id not in nodes:
            return -1
        node = nodes[node_id]
        if not node.get('dependsOn'):
            return 0
        dependson_levels = [compute_level(dependent_id) for dependent_id in node['dependsOn']]
        return max(dependson_levels) + 1

    max_level = 0
    for item in data:
        if item.get('group') == group or group == 'Любой':
            level = compute_level(item['key'])
            max_level = max(max_level, level)

    for level in range(max_level + 1):
        for item in data:
            if item.get('group') == group or group == 'Любой':
                if compute_level(item['key']) == level:
                    levels[level].append(item)

    for level, nodes in levels.items():
        res.append(nodes)

    return res

def calc_risks(list_of_issues: list, issue = None):
    if issue == None:
        issue = list_of_issues[0]

    list_of_parents = []
    for key in issue['dependsOn']:
        for dep_issue in list_of_issues:
            if dep_issue['key'] == key:
                list_of_parents.append(dep_issue)

    mean_spending_time = issue['cost'] * 24 * 60 * 60
    lambd = 1 / mean_spending_time

    start = issue['dateStart']
    startDate = None
    if start != None:
        startDate = datetime(int(start[:4]), int(start[5:7]), int(start[8:10]), 10, 0)

    end = issue['dateEnd']
    endDate = None
    if end != None:
        endDate = datetime(int(end[:4]), int(end[5:7]), int(end[8:10]), 10, 0)

    allocated_time = (endDate - startDate)
    allocated_time = allocated_time.days * 24 * 60 * 60 + allocated_time.seconds

    luck = 1
    if issue['status'] != 'closed':
        luck = 1 - exp(-lambd * allocated_time) # вероятность успеть
    for parent in list_of_parents:
        if parent['risk'] != None:
            luck *= 1 - parent['risk']
        else:
            luck *= 1 - calc_risks(list_of_issues, parent)

    risk = 1 - luck # риск - вероятность опоздать, от обратного

    issue['risk'] = risk

    return risk

def get_issues_from_tracker(group = 'Любой') -> list:
    res = []

    for issue in client.issues:
        if issue.queue.key == 'GYM':
            element = {}
            board_name = [board.name for board in client.boards if board.id == issue.boards[0]['id']][0]
            element['key'] = issue.key
            element['name'] = issue.summary
            element['group'] = board_name
            element['status'] = issue.status.key
            element['cost'] = issue.storyPoints
            element['risk'] = None # need to do
            element['url'] = "https://tracker.yandex.ru/" + issue.key
            element['dependsOn'] = get_depends_tasks(issue)
            element['dateStart'] = issue.start
            element['dateEnd'] = issue.deadline
            element['progress'] = calc_progress(issue.start, issue.deadline, issue.status.key)

            assignee = issue.assignee
            if assignee != None:
                assignee = assignee.display
            element['assignee'] = assignee

            res.append(element)

    for issue in res:
        calc_risks(res, issue)

    return filter_for_level(res, group)

def get_groups_from_tracker() -> list:
    res = [board.name for board in client.boards]
    res.remove('Gym')
    res.remove('Garbage')
    res.append('Любой')
    return res

@app.post("/upload/")
async def upload_csv(file: UploadFile = File(...)):
    if file.content_type == 'text/csv':
        try:
            csv_content = (await file.read()).decode('utf-8')
            data = parse_csv_with_multiple_parents(csv_content)
            put_data_to_tracker(data)
            return {'data': get_issues_from_tracker(), 'groups': get_groups_from_tracker()}
        except Exception as e:
            return {"error": f"Error processing CSV file: {str(e)}"}
    else:
        return {"error": "Incorrect file format. Please upload a CSV file."}

@app.post("/light_weight_baby/{group}")
async def get_new_data(group):
    try:
        return {'data': get_issues_from_tracker(group), 'groups': get_groups_from_tracker()}
    except Exception as e:
        return {"error": f"Error processing CSV file: {str(e)}"}


