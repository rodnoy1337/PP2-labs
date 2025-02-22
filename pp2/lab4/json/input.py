import json
f = open("sample.json")
print("Interface Status")
print("================================================================================")
print("DN                                                 Description           Speed    MTU  ")
print("-------------------------------------------------- --------------------  ------  ------")
link = json.loads(f.read())
cnt = 0
for i in link["imdata"]:
    if cnt == 3:
        break
    print(json.dumps(i["l1PhysIf"]["attributes"]["dn"]),
          end="                           ")
    print(json.dumps(i["l1PhysIf"]["attributes"]["speed"]), end=" ")
    print(json.dumps(i["l1PhysIf"]["attributes"]["mtu"]), end=" ")
    print()
    cnt += 1
