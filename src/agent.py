#!/usr/bin/env python3
from slnode import *
#from slnode import world_state

import json

rn = SlRosNode()

#slnode.__init__()
actionValues = {"0": 0.0, "1":0.1, "2":0.2, "3": 0.3, "4": 0.4, "5":0.5}
rn.SetActionValues(actionValues)
rn.run()
print(rn.world_state)
#slnode.run()

print("=====================")
rn.world_state["VehiclePosition"]
rn.world_state["VehicleVelocity"]
rn.world_state["ArmHeight"]
print("=====================")

#print(json.dumps(world_state, indent=4))
