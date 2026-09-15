# Double Tap - Half-Life inspired Sven Co-op prop

A fan-made interpretation of the classic Double Tap Root Beer machine: worn mustard enamel, a flat bevelled cabinet, metal waist, bottle hatch, projecting coin controls and rear ventilation. Original mesh and UVs; no ripped game assets.

## Install in Sven Co-op / J.A.C.K.

1. Copy the included `svencoop_addon` folder into your Sven Co-op game directory, merging folders.
2. Create a `cycler` point entity in J.A.C.K. using the Sven Co-op game profile.
3. Set its Model (`model`) to `models/zombies/doubletap_hl1.mdl`.
4. Leave Render Mode and Render FX at Normal. Skin 0; idle sequence 0.
5. Put the entity origin on the floor; at zero angles its front faces negative Y. Rotate to face the room.
6. Compile and load your map. Check the front, rear, lighting, floor contact and collision. This model compiled successfully but has not yet been tested in the game runtime.

Dimensions at scale 1: 43 units wide, 32.7 units deep, 77 units tall. Textures are embedded in the MDL; the loose texture files are only needed for editing. Add `models/zombies/doubletap_hl1.mdl` to your map's existing `.res` resource list when distributing it.

This is a static prop. Perk purchasing, power states, sounds and gameplay effects are not included. The READY and coin-price artwork is decorative. Configure collision deliberately when integrating the perk script; the mesh outline does not define exact collision.

## Included

- `svencoop_addon/models/zombies/doubletap_hl1.mdl` - compiled GoldSrc model.
- `doubletap_hl1.glb` - self-contained model for modern 3D software, Y-up metres.
- `model-viewer.html` - standalone interactive browser preview.
- `doubletap-preview.png` and `doubletap-turnaround.png` - rendered mesh previews, not game screenshots.
- `source/doubletap.obj`, `.mtl`, `.qc`, `doubletap_reference.smd`, `idle.smd` and `textures/` - editable model source, Z-up GoldSrc units.
- `source/build_doubletap.py` - geometry and texture builder; requires Python, NumPy and Pillow. Reads `front-art.png` in the parent folder.
- `compile-log.txt`, `validation.json`, `model-stats.json` - verification evidence.

To recompile, run the Sven Co-op SDK's `studiomdl.exe doubletap.qc` from the `source` folder. It writes into the included addon directory.

## Validation

316 triangles, 201 compiler-welded vertices, one bone, one stationary two-frame idle sequence. Four 256-colour diffuse textures: 128x256 front, 256x256 details and two 64x128 side/rear sheets.

Compiled using the installed StudioMDL SC (Dec 21 2020), with no reported errors or warnings. Independently checked IDST v10 headers, file length, embedded texture ranges, finite vertices, mesh indices, triangle counts and idle frames. Checked GLB geometry counts and container structure. Visually reviewed front, three-quarter and rear renders. Desktop and mobile viewer checks passed in headless Edge: controls, WebGL, download targets and horizontal layout. In-game playtest remains outstanding.

## Artwork

The front artwork was generated with the built-in image-generation tool and resized/quantized to an indexed texture. Other surfaces and the mesh were authored for this prop. Styling follows the classic yellow Double Tap machine and the muted paint, small diffuse textures and simple geometry of Half-Life 1. The previously created Juggernog model supplied the export pipeline.

Double Tap and the referenced game names belong to their respective owners. This is an unofficial fan-made model.
