##
# Copyright 2022 IBM Corp. All Rights Reserved.
#
# SPDX-License-Identifier: Apache-2.0
##

from lnn import Model, And, Variable, Predicate, Fact, Join

TRUE = Fact.TRUE


def test():
    join = Join.OUTER_PRUNED
    x, y, z, a, b = map(Variable, ("x", "y", "z", "a", "b"))

    # TEST 1

    # This is the normal 2 var vs 2 var ; should go thru the memory join
    p2 = Predicate("p2", 2)
    p2a = Predicate("p2a", 2)
    # p2_and_p2a = And(p2(x, y), p2a(y, z))

    p2a.add_data({("y1", "z1"): TRUE, ("y3", "z2"): TRUE})

    v1_before = p2.state()
    v2_before = p2a.state()

    # GT_o = dict(
    #     [
    #         (("x1", "y1", "z1"), TRUE),
    #         (("x1", "y1", "z2"), TRUE),
    #         (("x1", "y3", "z2"), TRUE),
    #         (("x2", "y2", "z1"), TRUE),
    #         (("x2", "y1", "z1"), TRUE),
    #         (("x2", "y2", "z2"), TRUE),
    #         (("x2", "y3", "z2"), TRUE),
    #     ]
    # )

    # p2_and_p2a.upward()

    v1_after = p2.state()
    v2_after = p2a.state()

    assert v1_after == v1_before, "FAILED 😔"
    assert v2_after == v2_before, "FAILED 😔"
    # assert all([p2_and_p2a.state(groundings=g) is GT_o[g] for g in GT_o]), "FAILED 😔"
    # assert len(p2_and_p2a.state()) == len(GT_o), "FAILED 😔"

    # TEST 2
    model = Model()

    t2_p3 = Predicate("t2_p3", 3)
    t2_p2 = Predicate("t2_p2", 2)
    t2_p3_and_t2_p2 = And(t2_p3(x, y, z), t2_p2(y, z))
    model.add_knowledge(t2_p3_and_t2_p2)
    model.add_data({t2_p3: {("x1", "y1", "z1"): TRUE, ("x3", "y3", "z3"): TRUE}})

    # GT_o = dict(
    #     [
    #         (("x1", "y1", "z1"), TRUE),
    #         (("x1", "y2", "z2"), TRUE),
    #         (("x3", "y1", "z1"), TRUE),
    #         (("x3", "y3", "z3"), TRUE),
    #         (("x3", "y2", "z2"), TRUE),
    #     ]
    # )

    v1_before = t2_p3.state()
    v2_before = t2_p2.state()

    # model.upward()

    v1_after = t2_p3.state()
    v2_after = t2_p2.state()

    assert v1_after == v1_before, "FAILED 😔"
    assert v2_after == v2_before, "FAILED 😔"
    # assert all(
    #     [t2_p3_and_t2_p2.state(groundings=g) is GT_o[g] for g in GT_o]
    # ), "FAILED 😔"
    # assert len(t2_p3_and_t2_p2.state()) == len(GT_o), "FAILED 😔"

    # TEST 3
    model = Model()
    t2_p3 = Predicate("t2_p3", 3)
    t2_p2 = Predicate("t2_p2", 2)
    t3_p1 = Predicate("t3_p1")
    t2_p3_and_t2_p2_t3_p1 = And(t2_p3(x, y, z), t2_p2(y, z), t3_p1(z))
    model.add_knowledge(t2_p3_and_t2_p2_t3_p1, join=join)
    model.add_data(
        {
            t2_p3: {("x1", "y1", "z1"): TRUE, ("x3", "y3", "z3"): TRUE},
            t2_p2: {("y1", "z1"): TRUE, ("y2", "z2"): TRUE},
            t3_p1: {"z1": TRUE, "z4": TRUE},
        }
    )
    v1_before = t2_p3.state()
    v2_before = t2_p2.state()
    v3_before = t3_p1.state()

    model.upward()

    v1_after = t2_p3.state()
    v2_after = t2_p2.state()
    v3_after = t3_p1.state()

    GT_o = dict(
        [
            (("x1", "y1", "z1"), TRUE),
            (("x1", "y2", "z2"), TRUE),
            (("x3", "y1", "z1"), TRUE),
            (("x3", "y3", "z3"), TRUE),
            (("x3", "y2", "z2"), TRUE),
            (("x1", "y2", "z1"), TRUE),
            (("x3", "y3", "z1"), TRUE),
            (("x3", "y2", "z1"), TRUE),
            (("x1", "y1", "z4"), TRUE),
            (("x1", "y2", "z4"), TRUE),
            (("x3", "y1", "z4"), TRUE),
            (("x3", "y3", "z4"), TRUE),
            (("x3", "y2", "z4"), TRUE),
        ]
    )

    assert v1_after == v1_before, "FAILED 😔"
    assert v2_after == v2_before, "FAILED 😔"
    assert v3_after == v3_before, "FAILED 😔"
    assert all(
        [t2_p3_and_t2_p2_t3_p1.state(groundings=g) is GT_o[g] for g in GT_o]
    ), "FAILED 😔"
    assert len(t2_p3_and_t2_p2_t3_p1.state()) == len(GT_o), "FAILED 😔"

    # TEST 4
    model = Model()

    t2_p3 = Predicate("t2_p3", 3)
    t2_p2 = Predicate("t2_p2", 2)
    t4_p1 = Predicate("t4_p1")

    t2_p3_and_t2_p2_t4_p1 = And(t2_p3(x, y, z), t2_p2(y, z), t4_p1(x))
    model.add_knowledge(t2_p3_and_t2_p2_t4_p1, join=join)

    model.add_data(
        {
            t2_p3: {("x1", "y1", "z1"): TRUE, ("x3", "y3", "z3"): TRUE},
            t2_p2: {("y1", "z1"): TRUE, ("y2", "z2"): TRUE},
            t4_p1: {"x1": TRUE, "x4": TRUE},
        }
    )

    v1_before = t2_p3.state()
    v2_before = t2_p2.state()
    v3_before = t4_p1.state()

    model.upward()

    v1_after = t2_p3.state()
    v2_after = t2_p2.state()
    v3_after = t4_p1.state()

    GT_o = dict(
        [
            (("x1", "y1", "z1"), TRUE),
            (("x1", "y2", "z2"), TRUE),
            (("x3", "y1", "z1"), TRUE),
            (("x3", "y3", "z3"), TRUE),
            (("x3", "y2", "z2"), TRUE),
            (("x1", "y3", "z3"), TRUE),
            (("x4", "y1", "z1"), TRUE),
            (("x4", "y3", "z3"), TRUE),
            (("x4", "y2", "z2"), TRUE),
        ]
    )

    assert v1_after == v1_before, "FAILED 😔"
    assert v2_after == v2_before, "FAILED 😔"
    assert v3_after == v3_before, "FAILED 😔"

    assert all(
        [t2_p3_and_t2_p2_t4_p1.state(groundings=g) is GT_o[g] for g in GT_o]
    ), "FAILED 😔"
    assert len(t2_p3_and_t2_p2_t4_p1.state()) == len(GT_o), "FAILED 😔"

    # TEST 5
    model = Model()
    t2_p3 = Predicate("t2_p3", 3)
    t2_p2 = Predicate("t2_p2", 2)
    t5_p2 = Predicate("t5_p2", 2)

    t2_p3_and_t2_p2_t5_p2 = And(t2_p3(x, y, z), t2_p2(y, z), t5_p2(a, b))
    model.add_knowledge(t2_p3_and_t2_p2_t5_p2, join=join)

    model.add_data(
        {
            t2_p3: {("x1", "y1", "z1"): TRUE, ("x3", "y3", "z3"): TRUE},
            t2_p2: {("y1", "z1"): TRUE, ("y2", "z2"): TRUE},
            t5_p2: {("a1", "b1"): TRUE, ("a2", "b2"): TRUE},
        }
    )

    v1_before = t2_p3.state()
    v2_before = t2_p2.state()
    v3_before = t5_p2.state()

    model.upward()

    v1_after = t2_p3.state()
    v2_after = t2_p2.state()
    v3_after = t5_p2.state()

    GT_o = dict(
        [
            (("x1", "y1", "z1", "a1", "b1"), TRUE),
            (("x1", "y2", "z2", "a1", "b1"), TRUE),
            (("x3", "y1", "z1", "a1", "b1"), TRUE),
            (("x3", "y3", "z3", "a1", "b1"), TRUE),
            (("x3", "y2", "z2", "a1", "b1"), TRUE),
            (("x1", "y1", "z1", "a2", "b2"), TRUE),
            (("x1", "y2", "z2", "a2", "b2"), TRUE),
            (("x3", "y1", "z1", "a2", "b2"), TRUE),
            (("x3", "y3", "z3", "a2", "b2"), TRUE),
            (("x3", "y2", "z2", "a2", "b2"), TRUE),
        ]
    )

    assert v1_after == v1_before, "FAILED 😔"
    assert v2_after == v2_before, "FAILED 😔"
    assert v3_after == v3_before, "FAILED 😔"
    assert all(
        [t2_p3_and_t2_p2_t5_p2.state(groundings=g) is GT_o[g] for g in GT_o]
    ), "FAILED 😔"
    assert len(t2_p3_and_t2_p2_t5_p2.state()) == len(GT_o), "FAILED 😔"


if __name__ == "__main__":
    test()
    print("success")
