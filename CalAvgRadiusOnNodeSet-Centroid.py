import numpy as np
from odbAccess import openOdb

# --- Configuration ---
odb_path = "RestartCycles_40-Partial-Openning-2Rows-Straight.odb"
instance_name = "TAPPEREDVESSEL-1"
target_node_set = "VESSEL-WIDER-PORTION"
step_name = "Load-160-C6"
frame_index = -1

# Restrict to the uniform cylindrical section (excluding partial end rings)
y_min_cut = 49.5  # mm
y_max_cut = 62.0  # mm
num_slices = 50 # binning parameter for numerical integration along the vessel.  Makeing sure not too small to no capture the overall curvature of the vessel.  And also not too large to have engouth nodes roughly span the entire circumference.

# Open ODB
odb = openOdb(odb_path, readOnly=True)
inst = odb.rootAssembly.instances[instance_name.upper()]

if target_node_set.upper() in inst.nodeSets.keys():
    target_nodes = inst.nodeSets[target_node_set.upper()].nodes
else:
    target_nodes = odb.rootAssembly.nodeSets[target_node_set.upper()].nodes[0]

step = odb.steps[step_name]
frame = step.frames[frame_index]
u_field = frame.fieldOutputs["U"]
u_dict = {val.nodeLabel: val.data for val in u_field.values}

# Extract 3D deformed coordinates within Y bounds
coords = []
for node in target_nodes:
    nid = node.label
    if nid in u_dict:
        x0, y0, z0 = node.coordinates
        u1, u2, u3 = u_dict[nid]
        y_def = y0 + u2
        if y_min_cut <= y_def <= y_max_cut:
            coords.append([x0 + u1, y_def, z0 + u3])

coords = np.array(coords)

# Slicing along Y
y_bins = np.linspace(y_min_cut, y_max_cut, num_slices + 1)

slice_avg, slice_min, slice_max = [], [], []

print("==========================================================")
print(" UNIFORM CYLINDER DEFORMED RADIUS ANALYSIS")
print(" Evaluated Y-Span: [{:.2f}, {:.2f}] mm".format(y_min_cut, y_max_cut))
print("==========================================================")

for i in range(len(y_bins) - 1):
    y_low, y_high = y_bins[i], y_bins[i + 1]
    mask = (coords[:, 1] >= y_low) & (coords[:, 1] < y_high)
    pts = coords[mask]

    # Only process complete cross-sectional rings (e.g. > 200 nodes)
    if len(pts) > 200:
        xc = np.mean(pts[:, 0])
        zc = np.mean(pts[:, 2])

        r_local = np.sqrt((pts[:, 0] - xc) ** 2 + (pts[:, 2] - zc) ** 2)

        slice_avg.append(np.mean(r_local))
        slice_min.append(np.min(r_local))
        slice_max.append(np.max(r_local))

print("Averaged Radius:  {:.6f} mm".format(np.mean(slice_avg)))
print("Min Radius:       {:.6f} mm".format(np.min(slice_min)))
print("Max Radius:       {:.6f} mm".format(np.max(slice_max)))
print("==========================================================")

odb.close()
