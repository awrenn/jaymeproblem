import pulp

##
## 5 week block
## ^ Do we care about this timespan?
## 5 PAs
## All PAs work a 40 hour week
## Shifts:
## M-F 5 shifts a day
## - 7-19 - 12
## - 19-7 - 12
## - 8-17 - 8
## - 8-12 - 4
## - 13-17 - 4
## Sunday:
## - 1 24hr
##
## Rules:
## Every 12-hour shift must be covered
## Every day, either 8 hour or 2 4 hours must be covered


def walk_node():
    pass


def main():
    prob = pulp.LpProblem("JaymesProblem")

    DAYS = range(5)
    dm = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

    PAS = range(5)
    pas = ["Jayme", "NotJayme" * 4]

    SHIFTS = range(5)
    shifts = ["Morning", "Night", "Full", "Half-Morn", "Half-ternoon"]

    SHIFT_COSTS = [12, 12, 8, 4, 4]

    choices = pulp.LpVariable.dicts("Coverage", (DAYS, PAS, SHIFTS), cat="Binary")
    uses_halfshifts = pulp.LpVariable.dicts("HalfShift", (DAYS,), cat="Binary")
    for day in DAYS:
        prob += pulp.lpSum([choices[day][p][0] for p in PAS]) == 1
        prob += pulp.lpSum([choices[day][p][1] for p in PAS]) == 1

        prob += (
            pulp.lpSum([choices[day][p][2] for p in PAS]) == 1 - uses_halfshifts[day]
        )

        prob += pulp.lpSum([choices[day][p][3] for p in PAS]) >= uses_halfshifts[day]
        prob += pulp.lpSum([choices[day][p][4] for p in PAS]) >= uses_halfshifts[day]

    prob += (
        pulp.lpSum([SHIFT_COSTS[s] * choices[d][0][s] for d in DAYS for s in SHIFTS])
        == 16
    )
    for pa in PAS[1:]:
        prob += (
            pulp.lpSum(
                [SHIFT_COSTS[s] * choices[d][pa][s] for d in DAYS for s in SHIFTS]
            )
            == 40
        )

    print(prob)
    solved = prob.solve()
    print(solved)

    hours = [24, 0, 0, 0, 0]
    for pa in PAS:
        for day in DAYS:
            for shift in SHIFTS:
                if pulp.value(choices[day][pa][shift]) == 1:
                    hours[pa] += SHIFT_COSTS[shift]
                    print(f"PA {pa} is working shift {shifts[shift]} on day {dm[day]}")
    print(hours)


if __name__ == "__main__":
    main()
