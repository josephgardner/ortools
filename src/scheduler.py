from __future__ import print_function
from ortools.constraint_solver import pywrapcp

def main():
  # Instantiate a cp solver.
  solver = pywrapcp.Solver('meal plan')
  
  num_weeks = 4
  num_days = 7 
  num_meals = 7 
  all_weeks = range(num_weeks)
  all_days = range(num_days)
  all_meals = range(num_meals)
  
  plan = {} 
  for week in all_weeks:
    for day in all_days:
      plan[(week, day)] = solver.IntVar(1, num_meals, "plan(%i,%i)" % (week, day))
  all_vars = [plan[(week, day)] for week in all_weeks for day in all_days]

  for week in all_weeks:
    solver.Add(solver.AllDifferent([plan[(week, day)] for day in all_days]))


  vars_phase = solver.Phase(all_vars,
                            solver.INT_VAR_SIMPLE,
                            solver.INT_VALUE_SIMPLE)

  solution = solver.Assignment()
  solution.Add(all_vars)
  collector = solver.FirstSolutionCollector(solution)

  # And solve.
  solver.Solve(vars_phase, [collector])

  if collector.SolutionCount() == 1:
    for week in all_weeks:
      print([int(collector.Value(0, plan[(week, day)])) for day in all_days])
  else:
    print('no solution')

if __name__ == '__main__':
  main()
