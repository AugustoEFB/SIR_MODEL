import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Cargar los datos
file_path = '/Users/Augusto/Desktop/SIR MODEL/data_covid-19_EU.csv'
data = pd.read_csv(file_path)

# Preprocesamiento de datos
data['dateRep'] = pd.to_datetime(data['dateRep'], format='%d/%m/%Y')
data = data.sort_values(['countriesAndTerritories', 'dateRep'])

# Seleccionar un país (ejemplo: Austria)
country = 'Austria'
data_country = data[data['countriesAndTerritories'] == country].copy()

# Calcular acumulados de casos y muertes
data_country['cum_cases'] = data_country['cases'].cumsum()
data_country['cum_deaths'] = data_country['deaths'].cumsum()

# Asumir recuperados (14 días después del caso)
data_country['recovered'] = data_country['cum_cases'].shift(14).fillna(0)

# Calcular infectados activos y susceptibles
N = data_country['popData2020'].iloc[0]
infected_initial = data_country['cum_cases'].iloc[0] - data_country['cum_deaths'].iloc[0]
recovered_initial = data_country['recovered'].iloc[0]
susceptible_initial = N - infected_initial - recovered_initial

# Definir el modelo SIR
def sir_model(y, t, N, beta, gamma):
    S, I, R = y
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    return [dSdt, dIdt, dRdt]

# Parámetros
beta = 0.116  # Tasa de contagio
gamma = 0.076  # Tasa de recuperación

# Resolver el modelo SIR
y0 = [susceptible_initial, infected_initial, recovered_initial]
t = np.linspace(0, len(data_country), len(data_country))  # Tiempo en días
solution = odeint(sir_model, y0, t, args=(N, beta, gamma))
S, I, R = solution.T

# Graficar los resultados
plt.figure(figsize=(12, 8))

# Gráfica del modelo SIR ajustado
plt.plot(t, S, label='Susceptibles (S)', color='blue')
plt.plot(t, I, label='Infectados (I)', color='red')
plt.plot(t, R, label='Recuperados (R)', color='green')
plt.title(f"Modelo SIR ajustado para {country}")
plt.xlabel('Días desde el inicio')
plt.ylabel('Población')
plt.legend()
plt.grid()
plt.show()
