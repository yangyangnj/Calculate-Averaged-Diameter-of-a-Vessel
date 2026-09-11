import numpy as np
from odbAccess import openOdb

# --- Configuration ---
odb_path = "RestartCycles_40-Partial-Openning-2Rows-Straight.odb"
instance_name = "TAPPEREDVESSEL-1"
#target_node_set = "VESSEL-WIDER-PORTION"
target_node_set = "AllNodes"
#step_name = "Unload-80-C6"
step_name = "Load-160-C6"
frame_index = -1

# Optional: Restrict Y-span to avoid incomplete boundary rings at the set edges
# Set to None to evaluate ALL nodes in the set directly
y_min_cut = 49.5  # mm
y_max_cut = 62.0  # mm

# Open ODB
odb = openOdb(odb_path, readOnly=True)
inst = odb.rootAssembly.instances[instance_name.upper()]

# Get nodes from target set
if target_node_set.upper() in inst.nodeSets.keys():
    target_nodes = inst.nodeSets[target_node_set.upper()].nodes
else:
    target_nodes = odb.rootAssembly.nodeSets[target_node_set.upper()].nodes[0]

# Get displacement field U
step = odb.steps[step_name]
frame = step.frames[frame_index]
u_field = frame.fieldOutputs["U"]
u_dict = {val.nodeLabel: val.data for val in u_field.values}

# Calculate deformed radius for each node relative to (0, 0)
radii_def = []

for node in target_nodes:
    nid = node.label
    if nid in u_dict:
        x0, y0, z0 = node.coordinates
        u1, u2, u3 = u_dict[nid]

        x_def = x0 + u1
        y_def = y0 + u2
        z_def = z0 + u3

        # Filter out boundary clipping if cuts are defined
        if (y_min_cut is not None) and not (y_min_cut <= y_def <= y_max_cut):
            continue

        # Direct radial calculation from (X=0, Z=0)
        r = np.sqrt(x_def**2 + z_def**2)
        radii_def.append(r)

radii_def = np.array(radii_def)

# Output Results
print("==================================================")
print(" Direct Deformed Radius Analysis: {}".format(instance_name))
print(" Target Set: {}".format(target_node_set))
print(" Step/Frame: {} / Frame[{}]".format(step_name, frame_index))
print("==================================================")
print(" Total Nodes Evaluated: {}".format(len(radii_def)))
print("--------------------------------------------------")
print(" Averaged Radius:  {:.6f} mm".format(np.mean(radii_def)))
print(" Min Radius:       {:.6f} mm".format(np.min(radii_def)))
print(" Max Radius:       {:.6f} mm".format(np.max(radii_def)))
print("==================================================")

odb.close()
