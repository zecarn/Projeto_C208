import streamlit as st
import pandas as pd
from simplex import solve_simplex

# Configuração inicial do Streamlit
st.set_page_config(page_title="Resolução de PPL com Simplex", page_icon="📊", layout="wide")
st.title("📊 Resolução de PPL com Simplex e Pós-Otimização")
st.markdown("---")

# Entrada da função objetivo
st.subheader("1️⃣ Configuração da Função Objetivo")
with st.container():
    # Configuração do número de variáveis
    num_variables = st.number_input("Número de variáveis:", min_value=2, max_value=5, step=1, value=3, help="Escolha o número de variáveis na função objetivo.")
    objective = []
    cols = st.columns(num_variables)
    for i, col in enumerate(cols):
        # Coletar os coeficientes da função objetivo
        coef = col.number_input(f"Coeficiente de x{i+1}:", value=0.0, key=f"objective_coef_{i}")
        objective.append(coef)

# Entrada das restrições
st.subheader("2️⃣ Configuração das Restrições")
with st.container():
    # Configuração do número de restrições
    num_constraints = st.number_input("Número de restrições:", min_value=1, max_value=5, step=1, value=2, help="Quantas restrições deseja adicionar?")
    constraints = []
    for i in range(num_constraints):
        st.markdown(f"**Restrição {i+1}**")
        cols = st.columns(num_variables + 1)
        # Coletar os coeficientes das variáveis e o limite da restrição
        coeffs = [cols[j].number_input(f"x{j+1} (Restrição {i+1})", value=0.0, key=f"constraint_{i}_var_{j}") for j in range(num_variables)]
        const = cols[-1].number_input(f"≤ Constante (Restrição {i+1})", value=0.0, key=f"constraint_const_{i}")
        constraints.append((coeffs, const))

# Entrada das alterações propostas para pós-otimização
st.subheader("3️⃣ Alterações Propostas (Pós-Otimização)")
with st.container():
    changes = []
    for i in range(num_constraints):
        # Coletar as alterações propostas nas restrições
        change = st.number_input(f"Alteração na restrição {i+1}:", value=0.0, key=f"change_{i}")
        changes.append(change)

# Resolver o problema ao clicar no botão
if st.button("🚀 Resolver PPL"):
    # Chamar a função do Simplex para resolver o problema
    solution, objective_value, new_objective_value, shadow_prices, feasibility = solve_simplex(objective, constraints, changes)

    # Exibir os resultados da otimização
    st.markdown("### 🟢 Resultados da Otimização")
    
    # Exibir o valor original da função objetivo
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Valor Original de Z (Função Objetivo)", f"R$ {objective_value:.2f}")
        
    # Exibir a solução ótima
    st.markdown("#### **Solução Ótima:**")
    solution_df = pd.DataFrame(solution.items(), columns=["Variável", "Valor"])
    st.table(solution_df)

    # Exibir os preços sombra das restrições
    st.markdown("### 🟡 Preços Sombra")
    shadow_prices_df = pd.DataFrame(shadow_prices.items(), columns=["Restrição", "Preço Sombra (R$)"])
    st.table(shadow_prices_df)

    st.markdown("---")
    st.markdown("### 🔵 Pós-Otimização")
    st.metric("Novo Valor de Z (Após Alterações)", f"R$ {new_objective_value:.2f}")


    # Exibir a viabilidade das alterações propostas
    feasibility_df = pd.DataFrame(
        {
            "Restrição": list(feasibility.keys()),
            "Viabilidade": ["Viável" if val >= 0 else "Não Viável" for val in feasibility.values()],
        }
    )
    st.markdown("#### **Viabilidade das Alterações Propostas:**")
    st.table(feasibility_df)
        # Calcular a diferença entre o valor original e o novo valor de Z
    delta_z = new_objective_value - objective_value

    # Exibir a mudança no lucro
    st.markdown("### 📊 Comparação do Lucro")
    if delta_z > 0:
        st.success(f"O lucro subiu em R$ {delta_z:.2f}")
    elif delta_z < 0:
        st.error(f"O lucro diminuiu em R$ {abs(delta_z):.2f}")
    else:
        st.info("O lucro permaneceu igual.")
