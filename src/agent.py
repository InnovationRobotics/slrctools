#!/usr/bin/env python3
import slnode
from slnode import world_state

import json

slnode.__init__()
print(world_state)
slnode.run()

print("=====================")
world_state["VehiclePosition"]
world_state["VehicleVelocity"]
world_state["ArmHeight"]
#print(json.dumps(world_state, indent=4))
