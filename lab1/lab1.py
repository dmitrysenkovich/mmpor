from ortools.linear_solver import pywraplp


def create_variable(solver, name):
    return solver.IntVar(0, solver.Infinity(), name)


def add_constraint(solver, variables, workers_count, is_needed):
    constraint = solver.Constraint(workers_count, solver.Infinity())
    for i in range(len(variables)):
        constraint.SetCoefficient(variables[i], is_needed[i])
    return constraint


def add_constraints(solver, variables):
    constraint1 = add_constraint(solver, variables, 16, [1, 0, 1, 0, 0, 0, 0, 0, 0])
    constraint2 = add_constraint(solver, variables, 30, [1, 0, 1, 1, 0, 0, 0, 0, 0])
    constraint3 = add_constraint(solver, variables, 31, [1, 1, 1, 1, 1, 0, 0, 0, 0])
    constraint4 = add_constraint(solver, variables, 45, [0, 1, 1, 1, 1, 1, 0, 0, 0])
    constraint5 = add_constraint(solver, variables, 66, [1, 1, 0, 1, 1, 1, 1, 0, 0])
    constraint6 = add_constraint(solver, variables, 72, [1, 0, 0, 0, 1, 1, 1, 1, 0])
    constraint7 = add_constraint(solver, variables, 61, [1, 1, 0, 0, 0, 1, 1, 1, 1])
    constraint8 = add_constraint(solver, variables, 34, [1, 1, 0, 0, 0, 0, 1, 1, 1])
    constraint9 = add_constraint(solver, variables, 16, [0, 1, 0, 0, 0, 0, 0, 1, 1])
    constraint10 = add_constraint(solver, variables, 10, [0, 1, 0, 0, 0, 0, 0, 0, 1])
    return [constraint1, constraint2, constraint3, constraint4, constraint5, constraint6, constraint7, constraint8, constraint9, constraint10]


def create_objective(solver, variables):
    objective = solver.Objective()
    objective.SetCoefficient(variables[0], 8 * 8)
    objective.SetCoefficient(variables[1], 8 * 8)
    objective.SetCoefficient(variables[2], 6 * 4)
    objective.SetCoefficient(variables[3], 7 * 4)
    objective.SetCoefficient(variables[4], 9 * 4)
    objective.SetCoefficient(variables[5], 10 * 4)
    objective.SetCoefficient(variables[6], 8 * 4)
    objective.SetCoefficient(variables[7], 6 * 4)
    objective.SetCoefficient(variables[8], 6 * 4)
    objective.SetMinimization()
    return objective


def create_solver():
    solver = pywraplp.Solver(
        'SolveIntegerProblem',
        pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING,
    )

    # 9-12, 11-14, 9-13, 10-14, 11-15, 12-16, 13-17, 14-18, 15-19
    variables = [create_variable(solver, 'worker_' + str(i)) for i in range(0, 9)]
    constraints = add_constraints(solver, variables)
    objective = create_objective(solver, variables)
    return solver, variables, constraints, objective


def solve(solver, variables, objective):
    result = solver.Solve()
    optimal = result == pywraplp.Solver.OPTIMAL
    verified = 0
    if optimal:
        verified = solver.VerifySolution(1e-4, True)

    if not optimal or not verified:
        return

    for variable in variables:
        print("worker {}: {}".format(variable.name(), variable.solution_value()))

    print("target: {}".format(objective.Value()))


def main():
    solver, variables, constraints, objective = create_solver()
    solve(solver, variables, objective)
    print()

    solver, variables, constraints, objective = create_solver()
    fulltime_workers_min_count_constraint = solver.Constraint(4, solver.Infinity())
    fulltime_workers_min_count_constraint.SetCoefficient(variables[0], 1)
    fulltime_workers_min_count_constraint.SetCoefficient(variables[1], 1)
    constraints.append(fulltime_workers_min_count_constraint)
    solve(solver, variables, objective)
    print()

    solver, variables, constraints, objective = create_solver()
    workers_max_count_constraint = solver.Constraint(0, 94)
    for variable in variables:
        workers_max_count_constraint.SetCoefficient(variable, 1)
    constraints.append(workers_max_count_constraint)
    solve(solver, variables, objective)


if __name__ == '__main__':
    main()
    