from yandex_tracker_client import TrackerClient
from datetime import datetime, timedelta

client = TrackerClient(token="y0_AgAAAAAUf2HOAAt_cgAAAAD_OQTuAAA-mPvZ6hpEjq9TA0T0yC30vzNXSQ", cloud_org_id="bpfud6rvc4vqm8f4qpu6")
print([issue.key for issue in client.issues.find('Queue: GYM')])

issue = client.issues['GYM-84']

# try:
#     issue.links.create(issue='GYM-81', relationship='is dependent by')
# except Exception as e:
#     print(e.args[0].status_code)

print([field.key for field in client.fields])
print(issue.statusStartTime)
print(issue.end)
print(issue.deadline)

date = "2024-04-24T07:46:44"
h = 0
m = 0

y = int(date[:4])
mo = int(date[5:7])
d = int(date[8:10])
if len(date) > 10:
    h = int(date[11:13])
    m = int(date[14:16])

print((datetime.now() - datetime(y, mo, d, h, m)).days)

print([[link.object.key, link.direction, link.type.id] for link in issue.links])