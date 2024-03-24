from yandex_tracker_client import TrackerClient

client = TrackerClient(token="y0_AgAAAAAUf2HOAAt_cgAAAAD_OQTuAAA-mPvZ6hpEjq9TA0T0yC30vzNXSQ", cloud_org_id="bpfud6rvc4vqm8f4qpu6")
print([issue.key for issue in client.issues.find('Queue: GYM')])

issue = client.issues['GYM-45']

print([field.key for field in client.fields])
print([issue.start for issue in client.issues])