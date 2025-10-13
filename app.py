import pandas as pd
import scipy.stats
import streamlit as st

# Variables de estado
if 'experiment_no' not in st.session_state:
    st.session_state['experiment_no'] = 0

if 'df_experiment_results' not in st.session_state:
    st.session_state['df_experiment_results'] = pd.DataFrame(columns=['no', 'iteraciones', 'media'])

st.header('Lanzar una moneda')

def toss_coin(n):
    """Simula lanzar una moneda n veces y devuelve la media acumulada."""
    trial_outcomes = scipy.stats.bernoulli.rvs(p=0.5, size=n)
    outcome_1_count = 0
    means = []

    for i, r in enumerate(trial_outcomes, start=1):
        if r == 1:
            outcome_1_count += 1
        mean = outcome_1_count / i
        means.append(mean)

    return means

# Interfaz
number_of_trials = st.slider('¿Número de intentos?', 1, 1000, 10, key='slider_trials')
start_button = st.button('Ejecutar', key='start_button')

if start_button:
    st.write(f'Experimento con {number_of_trials} intentos en curso.')
    st.session_state['experiment_no'] += 1
    means = toss_coin(number_of_trials)

    # Mostrar gráfico una sola vez
    st.line_chart(means)

    # Guardar resultado final
    final_mean = means[-1]
    st.session_state['df_experiment_results'] = pd.concat([
        st.session_state['df_experiment_results'],
        pd.DataFrame([[st.session_state['experiment_no'], number_of_trials, final_mean]],
                     columns=['no', 'iteraciones', 'media'])
    ], axis=0).reset_index(drop=True)

st.write(st.session_state['df_experiment_results'])
