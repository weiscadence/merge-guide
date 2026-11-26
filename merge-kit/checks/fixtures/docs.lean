import Mathlib.Data.Nat.Basic

/-- The doubling map. -/
def documented (n : ℕ) : ℕ := 2 * n

def undocumented (n : ℕ) : ℕ := 3 * n

/-- Matches the roadmap `Suggested.lean` signature. -/
theorem documented_pos (n : ℕ) (h : 0 < n) : 0 < documented n := by
  unfold documented; omega
