/-! Exact band-edge sign lemmas for the repository's S1–S6 model.
These do not imply a physical SOC band inversion or Berry invariant. -/
namespace BismuthBandEdge

def gap (ec ev : Int) : Int := ec - ev

theorem semiconductor_gap : gap 55 (-55) = 110 := by decide
theorem semimetal_gap : gap (-2) 2 = -4 := by decide
theorem semiconductor_positive : 0 < gap 55 (-55) := by decide
theorem semimetal_negative : gap (-2) 2 < 0 := by decide
theorem overlap_positive : 0 < -(gap (-2) 2) := by decide

def electronPocket (ec ef : Int) : Int := max (ef - ec) 0
def holePocket (ev ef : Int) : Int := max (ev - ef) 0

theorem semiconductor_empty_pockets :
    electronPocket 55 0 = 0 ∧ holePocket (-55) 0 = 0 := by decide
theorem semimetal_both_pockets :
    electronPocket (-2) 0 = 2 ∧ holePocket 2 0 = 2 := by decide

theorem gap_sign_not_mass_sign :
    gap (-2) 2 = -4 ∧ gap 55 (-55) = 110 := by decide

end BismuthBandEdge

#print axioms BismuthBandEdge.semiconductor_gap
#print axioms BismuthBandEdge.semimetal_gap
#print axioms BismuthBandEdge.semiconductor_empty_pockets
#print axioms BismuthBandEdge.semimetal_both_pockets
