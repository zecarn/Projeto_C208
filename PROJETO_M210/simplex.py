from pulp import LpProblem, LpMaximize, LpVariable, value

def solve_simplex(objective, constraints, changes):

    # Criar o problema de maximização
    problem = LpProblem("Problema_PPL", LpMaximize)

    # Criar variáveis de decisão com limite inferior de 0
    variables = {f"x{i+1}": LpVariable(f"x{i+1}", lowBound=0) for i in range(len(objective))}

    # Adicionar a função objetivo ao problema
    problem += sum(objective[i] * variables[f"x{i+1}"] for i in range(len(objective)))

    # Adicionar as restrições ao problema
    for idx, (coeffs, const) in enumerate(constraints):
        problem += sum(coeffs[i] * variables[f"x{i+1}"] for i in range(len(coeffs))) <= const, f"Restrição_{idx+1}"

    # Resolver o problema
    problem.solve()

    # Capturar a solução ótima (valores das variáveis)
    solution = {var.name: var.varValue for var in problem.variables()}

    # Capturar o valor da função objetivo original
    objective_value = value(problem.objective)

    # Capturar os preços sombra de cada restrição
    shadow_prices = {f"Restrição_{i+1}": problem.constraints[f"Restrição_{i+1}"].pi for i in range(len(constraints))}

    # Calcular a viabilidade das alterações nas restrições
    feasibility = {
        f"Restrição_{i+1}": shadow_prices[f"Restrição_{i+1}"] * changes[i] + constraints[i][1]
        for i in range(len(constraints))
    }

    # Calcular o novo valor da função objetivo com as alterações propostas
    delta_z = sum(shadow_prices[f"Restrição_{i+1}"] * changes[i] for i in range(len(constraints)))
    new_objective_value = objective_value + delta_z

    return solution, objective_value, new_objective_value, shadow_prices, feasibility