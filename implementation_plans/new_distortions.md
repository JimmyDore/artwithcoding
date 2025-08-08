## New Distortion Types – Implementation Plan

### Goal
Add a few visually compelling distortion types to `DistortionType` and implement them in `DistortionEngine`, with comprehensive unit tests and integration coverage.

### Proposed New Distortion Types
- **SWIRL (`"swirl"`)**: Rotational swirl around the canvas center. Angle depends on distance to center and time, creating vortex-like motion.
- **RIPPLE (`"ripple"`)**: Concentric waves emanating from the center, but applied along the tangential direction (perpendicular to radius) to differentiate from radial displacement.
- **FLOW (`"flow"`)**: Time-evolving flow-field (pseudo curl-noise) that advects points using a smooth, coherent vector field of sin/cos combinations.

### Acceptance Criteria
- `DistortionType` includes the new values: `swirl`, `ripple`, `flow`.
- `DistortionEngine` implements: `apply_distortion_swirl`, `apply_distortion_ripple`, `apply_distortion_flow`.
- `get_distorted_positions` routes the new types correctly.
- Unit tests:
  - Updated enum tests for `DistortionType` (values and count).
  - New tests that validate each new distortion returns a valid `(x, y, rotation)` and handles edge cases (e.g., center point for swirl/ripple).
  - Parametrized tests include new types.
- Integration: iteration over all `DistortionType` works with `DeformedGrid`.
- ColorScheme enum aligns with existing color generation functionality and tests.

### Steps
1. Update `enums.py`:
   - Add `SWIRL`, `RIPPLE`, `FLOW` to `DistortionType`.
   - Align `ColorScheme` members to match tested set (10 values): `monochrome`, `gradient`, `rainbow`, `complementary`, `temperature`, `pastel`, `neon`, `ocean`, `fire`, `forest`.
2. Implement new distortion functions in `distorsion_movement/distortions.py`:
   - `apply_distortion_swirl(base_pos, params, cell_size, distortion_strength, time, canvas_size)`
   - `apply_distortion_ripple(base_pos, params, cell_size, distortion_strength, time, canvas_size)`
   - `apply_distortion_flow(base_pos, params, cell_size, distortion_strength, time)`
   - Update `get_distorted_positions` to route new types.
3. Update tests:
   - Modify `tests/test_enums.py` to reflect new `DistortionType` values and count; ensure `ColorScheme` count/values match.
   - Extend `tests/test_distortions.py` with tests for `swirl`, `ripple`, `flow`, and expand parametrized coverage.
4. Run test suite and fix any issues.
5. Document briefly in `README.md` (optional in this iteration).

### Notes
- Keep distortion outputs bounded using `cell_size * distortion_strength` as the primary magnitude scale, consistent with existing patterns.
- Handle singularities gracefully: at exact canvas center for center-based effects, return original position and zero rotation.

