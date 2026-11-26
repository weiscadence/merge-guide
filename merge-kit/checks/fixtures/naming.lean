/-! Fixture for checks/naming.py -/

theorem FooBarBaz (n : ℕ) : n = n := rfl

theorem foo_iff (n : ℕ) (h : 0 < n) : n ≠ 0 := by omega

theorem coe_apply (f : α →+ β) (x : α) : ⇑f x = f x := rfl

namespace Polynomial

theorem bound_of_pos (x : ℝ) (hx : 0 < x) : 0 < x ^ 2 := by positivity

end Polynomial

lemma good_name (n : ℕ) : n + 0 = n := rfl

structure my_struct where
  x : ℕ
