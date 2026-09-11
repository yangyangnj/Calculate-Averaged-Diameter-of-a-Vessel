# Calculate-Averaged-Diameter-of-a-Vessel
# Abaqus ODB Deformed Radius Calculator

A lightweight Python post-processing script for Abaqus ODB files that calculates the deformed cross-sectional radius of cylindrical or tapered vessel models (e.g., shell/solid structures) under deformation or pulsatile loading.

---

### Features

* **Direct Coordinate Calculation:** Computes the deformed radial distance $r = \sqrt{X_{\text{def}}^2 + Z_{\text{def}}^2}$ directly relative to the central global axis $(X=0, Z=0)$.
* **Label-Bound Nodal Displacement:** Maps nodal displacement output vectors (`U1`, `U2`, `U3`) strictly to matching `OdbMeshNode` labels to prevent indexing or coordinate mismatch errors.
* **Axial Boundary Filtering:** Includes optional axial ($Y$-axis) clipping to exclude boundary effects, partial edge rings, or transition regions.
* **Flexible Node Set Targeting:** Supports targeting specific instance node sets (e.g., `VESSEL-WIDER-PORTION`) or assembly-level node sets (e.g., `AllNodes`).

---

### Prerequisites

* **Abaqus Environment:** Runs using the Abaqus Python interpreter (`abq2023` or equivalent).
* **Python Libraries:** Requires standard Abaqus extraction modules (`odbAccess`) and `numpy`.

---

### Configuration Parameters

Edit the top section of `CalAvgRadiusOnNodeSet-NoCentroid.py` to match your simulation setup:

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `odb_path` | `str` | File path to the `.odb` file. |
| `instance_name` | `str` | Name of the target part instance (e.g., `TAPPEREDVESSEL-1`). |
| `target_node_set` | `str` | Target node set name (e.g., `AllNodes` or `VESSEL-WIDER-PORTION`). |
| `step_name` | `str` | Analysis step to process (e.g., `Load-160-C6`). |
| `frame_index` | `int` | Frame index within the step (`-1` evaluates the final frame). |
| `y_min_cut` | `float` or `None` | Minimum $Y$-coordinate boundary filter (in mm). |
| `y_max_cut` | `float` or `None` | Maximum $Y$-coordinate boundary filter (in mm). |

---

### Usage

Run the script directly through the Abaqus Python execution interface:

```bash
abq2023 python CalAvgRadiusOnNodeSet-NoCentroid.py

==================================================
 Direct Deformed Radius Analysis: TAPPEREDVESSEL-1
 Target Set: AllNodes
 Step/Frame: Load-160-C6 / Frame[-1]
==================================================
 Total Nodes Evaluated: 11880
--------------------------------------------------
 Averaged Radius:  9.141723 mm
 Min Radius:       8.890912 mm
 Max Radius:       9.508104 mm
==================================================
