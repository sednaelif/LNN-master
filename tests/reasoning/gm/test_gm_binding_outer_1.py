##
# Copyright 2022 IBM Corp. All Rights Reserved.
#
# SPDX-License-Identifier: Apache-2.0
##

from lnn import Model, And, Variable, Predicate, Fact, Join


def test():
    join = Join.OUTER
    model = Model()
    x, y, z, a, b = map(Variable, ("x", "y", "z", "a", "b"))

    # TEST 1

    # This is the normal 2 var vs 2 var ; should go thru the memory join
    p2 = Predicate("p2", 2)
    p2.add_data({("x1", "y1"): Fact.TRUE, ("x2", "y2"): Fact.TRUE})

    p2a = Predicate("p2a", 2)
    p2a.add_data({("y1", "z1"): Fact.TRUE, ("y3", "z2"): Fact.TRUE})

    # print("Predicates before outer Join")

    # GT_i = dict([
    #    (('x1', 'y1', 'z1'), Fact.TRUE)])

    GT_o = dict(
        [
            (("x1", "y1", "z2"), Fact.UNKNOWN),
            (("x1", "y3", "z2"), Fact.UNKNOWN),
        ]
    )
    p2_and_p2a = And(p2(x, y, bind={x: "x1"}), p2a(y, z, bind={z: "z2"}), join=join)
    model.add_knowledge(p2_and_p2a)
    p2_and_p2a.upward()
    model.print()

    assert all([p2_and_p2a.state(groundings=g) is GT_o[g] for g in GT_o]), "FAILED 😔"
    assert len(p2_and_p2a.state()) == len(GT_o), "FAILED 😔"
    model.flush()


if __name__ == "__main__":
    test()
    print("success")
