/-! Fixture for checks/hygiene.py. The word sorry in this comment must not count. -/

set_option maxHeartbeats 400000 in
theorem slow : True := by
  sorry

#eval 1 + 1

theorem long_line_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa : True := trivial
