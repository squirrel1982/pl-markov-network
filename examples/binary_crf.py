# Demonstrates parameter estimation for small discrete systems using
# MLE as well as MPLE, and compares the quality of the weights using the 
# true probability mass of each assignment as a reference.

from plmrf import *
import numpy as np

nsamp = 1000
x1 = np.random.binomial(1, 0.5, nsamp)
y1 = np.random.binomial(1, x1 * 0.8 + (1 - x1) * 0.2, nsamp)

x2 = np.random.binomial(1, 0.5, nsamp)
y2 = np.random.binomial(1, x2 * 0.8 + (1 - x2) * 0.2, nsamp)

var_defs = [
    VariableDef("y1", ddomain=[0, 1]),
    VariableDef("y2", ddomain=[0, 1])
]

potentials = [
    BinaryProductPotential(["x1", "y1"]),
    BinaryProductPotential(["x2", "y2"]),
    BinaryProductPotential(["y1", "y2"]),
    BinaryProductPotential(["y1"]),
    BinaryProductPotential(["y2"])
]

data = {
    "x1" : x1,
    "x2" : x2,
    "y1" : y1,
    "y2" : y2,
}

network = LogLinearMarkovNetwork(potentials, var_defs, 
    tied_weights=[[0, 1], [3, 4]], conditioned={"y1" : ["x1"], "y2" : ["x2"]})

conditions = {"x1" : 1, "x2" : 0}
all_combos = network.expand_joint(conditions=conditions)
x1p, x2p, y1p, y2p = (all_combos["x1"], all_combos["x2"], all_combos["y1"], all_combos["y2"])
true_probs= (
    ((y1p == x1p) * 0.8 + (1 - (y1p == x1p)) * 0.2) * 
    ((y2p == x2p) * 0.8 + (1 - (y2p == x2p)) * 0.2)
    )

mple_result = network.fit(data)
mple_probs = network.normalized_prob(all_combos)
print(mple_probs)
mple_pseudo_probs = network.pseudonormalized_prob(all_combos)

print("-----------------------")
print("MPLE result:")
print("-----------------------")
print(mple_result)

results = np.column_stack((true_probs, mple_probs, mple_pseudo_probs, x1p, x2p, y1p, y2p))
np.savetxt(sys.stdout, results, fmt="%.4f", delimiter="\t", 
    header=", ".join(["True Probs", "MPLE Probs", "MPLE Pseudo-probs", "X1", "X2", "Y1", "Y2"]))



