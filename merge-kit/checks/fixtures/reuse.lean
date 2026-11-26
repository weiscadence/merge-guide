/-! Fixture for checks/reuse.py -/

noncomputable def rationalificationMap (V : Type) [AddCommGroup V] : V →+ ℚ ⊗[ℤ] V :=
  (TensorProduct.mk ℤ ℚ V 1).toAddMonoidHom

theorem rationalificationMap_injective (V : Type) [AddCommGroup V] [Module.Flat ℤ V] :
    Function.Injective (rationalificationMap V) := by
  exact Module.Flat.tensorProduct_mk_injective _ _ _

theorem unrelated_thing (q : Quux) : Quux.frob q = Quux.frob q := rfl
