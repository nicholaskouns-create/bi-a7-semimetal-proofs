From Coq Require Import ZArith Lia.
Open Scope Z_scope.

Definition gap (ec ev : Z) : Z := ec - ev.
Definition electron_pocket (ec ef : Z) : Z := Z.max (ef - ec) 0.
Definition hole_pocket (ev ef : Z) : Z := Z.max (ev - ef) 0.

Theorem semiconductor_gap : gap 55 (-55) = 110.
Proof. unfold gap; lia. Qed.
Theorem semimetal_gap : gap (-2) 2 = -4.
Proof. unfold gap; lia. Qed.
Theorem semiconductor_positive : 0 < gap 55 (-55).
Proof. unfold gap; lia. Qed.
Theorem semimetal_negative : gap (-2) 2 < 0.
Proof. unfold gap; lia. Qed.
Theorem overlap_positive : 0 < -(gap (-2) 2).
Proof. unfold gap; lia. Qed.
Theorem semiconductor_empty_pockets :
  electron_pocket 55 0 = 0 /\ hole_pocket (-55) 0 = 0.
Proof. unfold electron_pocket, hole_pocket; vm_compute; auto. Qed.
Theorem semimetal_both_pockets :
  electron_pocket (-2) 0 = 2 /\ hole_pocket 2 0 = 2.
Proof. unfold electron_pocket, hole_pocket; vm_compute; auto. Qed.

Print Assumptions semiconductor_gap.
Print Assumptions semimetal_gap.
Print Assumptions semiconductor_empty_pockets.
Print Assumptions semimetal_both_pockets.
