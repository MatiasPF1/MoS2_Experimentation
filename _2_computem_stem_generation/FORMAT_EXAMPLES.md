# COMPUTEM/AUTOSTEM File Format Examples

## XYZ File Format

### Structure
```
Line 1: Description/comment line
Line 2: ax  by  cz  (unit cell dimensions in Angstroms)
Line 3+: Z  x  y  z  occupancy  [wobble]
Last line: -1  (signals end of file)
```

### Column Definitions
- **Z**: Atomic number (6=Carbon, 16=Sulfur, 42=Molybdenum, etc.)
- **x, y, z**: Atomic coordinates in Angstroms
- **occupancy**: Site occupancy (0.0 to 1.0, typically 1.0 for fully occupied)
- **wobble**: RMS thermal displacement in Angstroms (optional, defaults to 0.0)

### Example 1: Graphene (from graphene.xyz)
```
one unit cell of graphene
2.456   4.2539168   3.3480
6  0.0000  0.0000      1.6740  1.0
6  1.2280  0.70898613  1.6740  1.0
6  1.2280  2.12695839  1.6740  1.0
6  2.4560  2.83594452  1.6740  1.0
-1
```

### Example 2: MoS2 Single Unit Cell
```
MoS2_unit_cell_Created_at_2025_12_25_10_30_00
3.1600  5.4737  6.1000
42  0.000000  0.000000  3.050000  1  0.08
16  1.580000  0.912283  0.000000  1  0.08
16  1.580000  0.912283  6.100000  1  0.08
-1
```

### Example 3: MoS2 with Defects
```
MoS2_incostem_10_10_1_Created_at_2025_12_25_10_30_15
31.600  54.737  6.100
42  0.000000  0.000000  3.050000  1  0.08
16  1.580000  0.912283  0.000000  1  0.08
16  1.580000  0.912283  6.100000  1  0.08
42  1.580000  2.736850  3.050000  1  0.08
16  3.160000  3.649133  0.000000  1  0.08
16  3.160000  3.649133  6.100000  1  0.08
74  3.160000  0.000000  3.050000  1  0.08
16  4.740000  0.912283  0.000000  1  0.08
17  4.740000  0.912283  6.100000  1  0.08
...more atoms...
-1
```

---

## PARAM File Format

### Structure (Interactive Input Order)
```
Line 1: input.xyz
Line 2: ncellx ncelly ncellz  (replication, usually: 1 1 1)
Line 3: output.tif
Line 4: nx ny  (transmission function size in pixels)
Line 5: keV Cs3 Cs5 df apert1 apert2  (microscope parameters)
Line 6: almin almax detector_type  (detector configuration)
Line 7: END  (end of higher order aberrations)
Line 8: sourceFWHM  (source size in Angstroms)
Line 9: defocus_spread  (in Angstroms)
Line 10: y/n  (counting noise yes/no)
Line 11: probe_current dwell_time  (if counting noise = y)
Line 12: -1  (end of file)
```

### Parameter Details

**Microscope Parameters (Line 5):**
- `keV`: Beam energy in keV (e.g., 80, 100, 200, 300)
- `Cs3`: Spherical aberration in mm (typically 0.001 to 5)
- `Cs5`: 5th order aberration in mm (typically 0 to 10)
- `df`: Defocus in Angstroms (e.g., -100 to +100)
- `apert1`: Inner aperture angle in mrad (typically 0)
- `apert2`: Outer aperture angle in mrad (e.g., 15 to 30)

**Detector Configuration (Line 6):**
- `almin`: Inner detector angle in mrad
- `almax`: Outer detector angle in mrad
- `detector_type`: 
  - `m` or `M` = ADF (Annular Dark Field)
  - `a` or `A` = Confocal
  - `seg` or `SEG` = Segmented detector (requires phimin phimax)
  - `com` or `COM` = Center of Mass

**Common Detector Angles:**
- Bright Field: 0 to 10 mrad
- ADF: 60 to 200 mrad
- HAADF: 100 to 300 mrad

### Example 1: Basic STEM Image (with counting noise)
```
MoS2_incostem_10_10_1_0.xyz
1 1 1
ImageMoS2_incostem_10_10_1_0.tif
512 512
200 1.5 0 -50 0 25
60 200 m
END
0.8
15.0
y
0.05 0.000001
-1
```

### Example 2: Label/Defect Map (no counting noise)
```
MoS2_2Doped_incostem_10_10_1_0.xyz
1 1 1
2Doped_MoS2_incostem_10_10_1_0.tif
512 512
200 1.5 0 -50 0 25
60 200 m
END
0.8
15.0
n
-1
```

### Example 3: Multiple Detectors
```
sample.xyz
1 1 1
output.tif
256 256
100 0.5 0 0 0 20
0 10 m
60 200 m
100 300 m
END
0.5
10.0
y
0.1 0.000002
-1
```

### Example 4: High Resolution with Aberrations
```
highres_sample.xyz
1 1 1
highres_output.tif
1024 1024
300 0.001 0 -25 0 30
80 200 m
END
0.3
5.0
y
0.08 0.0000005
-1
```

---

## Relationship Between Files

### Generation.py creates:
1. **XYZ files**: Atomic coordinates with defects
2. **PARAM files**: Microscope/detector settings
3. **BATCH file**: Commands to run all simulations

### Batch File Format
```batch
incostem.exe<MoS2_incostem_10_10_1_0.param
incostem.exe<MoS2_metal_Doped_incostem_10_10_1_0.param
incostem.exe<MoS2_2Doped_incostem_10_10_1_0.param
...etc
```

### Execution Flow
```
1. Generate XYZ + PARAM files (Generation.py)
   ↓
2. Run batch file with incostem.exe
   ↓
3. Produces TIFF image files
   ↓
4. Pre-process images (normalize, resize, etc.)
   ↓
5. Feed to ML model
```

---

## Important Notes

### XYZ File Notes:
- Empty lines and lines starting with `#` are ignored
- The wobble parameter is optional (defaults to 0.0)
- Coordinates are in Angstroms
- Must end with `-1`
- Unit cell dimensions (ax, by, cz) define the periodic boundaries

### PARAM File Notes:
- All angles in **mrad** (milli-radians)
- Lengths in **Angstroms** except Cs3/Cs5 which are in **mm**
- Must end with `-1`
- Counting noise requires probe current (electrons/Angstrom²) and dwell time (seconds)
- Multiple detectors can be specified (one per line before END)

### Common Mistakes to Avoid:
1. ❌ Forgetting `-1` at end of files
2. ❌ Wrong units (e.g., Cs in Angstroms instead of mm)
3. ❌ Missing detector type (m, a, seg, com)
4. ❌ Not matching XYZ filename in PARAM file
5. ❌ Probe current/dwell time when counting noise is 'n'
