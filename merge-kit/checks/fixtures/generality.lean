/-! Fixture for checks/generality.py -/

theorem inv_thing (t : ℝ) (ht : 0 < t) : t * t⁻¹ = 1 := mul_inv_cancel₀ ht.ne'

theorem ring_only {K : Type} [Field K] (a b : K) : a + b = b + a := add_comm a b

theorem keeps_field {K : Type} [Field K] (a : K) (h : a ≠ 0) : a * a⁻¹ = 1 := mul_inv_cancel₀ h

theorem natDegree_minpoly_inv' (x : F) : (minpoly ℚ x⁻¹).natDegree = (minpoly ℚ x).natDegree := by
  exact foo x

section

variable {𝕜 : Type} [RCLike 𝕜]

theorem norm_mul_thing (a b : 𝕜) : ‖a * b‖ = ‖a‖ * ‖b‖ := norm_mul a b

end
