# SIR Model Analysis Using COVID-19 Data from the European Centre for Disease Prevention and Control

---

## Introduction
This repository contains Python code implementing the **Susceptible-Infected-Recovered (SIR)** model for epidemiological analysis. The data used spans from 2020 to 2022 and was obtained from the **European Centre for Disease Prevention and Control (ECDC)**. Each row in the dataset represents daily new cases and deaths reported for countries within the EU/EEA. The SIR model provides insights into the progression of the COVID-19 pandemic in various countries.

The recovery period (\(R\)) is assumed to last **14 days**, based on guidelines from the **World Health Organization (WHO)**, which state that COVID-19 symptoms generally resolve within 1 to 14 days.

---

## Methodology

### Data Preprocessing
- The dataset includes daily new cases, deaths, and population data for multiple countries.
- Dates are converted to Python’s datetime format, and data is sorted chronologically by country.
- Cumulative cases, deaths, and recovered individuals are calculated as follows:
  1. **Recovered**: Calculated by shifting cumulative cases (`cum_cases`) by 14 days.
  2. **Active infected**: \( 	ext{Active Infected} = \text{cum\_cases} - \text{cum\_deaths} - \text{recovered} \).
  3. **Susceptible population**: \( 	ext{Susceptible} = N - 	ext{infected} - 	ext{recovered} \), where \( N \) is the total population.

### Model Implementation
- The SIR model equations are:
  ```
  dS/dt = -beta * S * I / N
  dI/dt = beta * S * I / N - gamma * I
  dR/dt = gamma * I
  ```
  - Here:
    - \( S \): Number of susceptible individuals.
    - \( I \): Number of infected individuals.
    - \( R \): Number of recovered individuals.
    - \( \beta \): Infection rate.
    - \( \gamma \): Recovery rate.
    - \( N \): Total population.
- Parameters \( \beta \) (infection rate) and \( \gamma \) (recovery rate) are estimated using **nonlinear least squares** with the `scipy.optimize.curve_fit` method.

### Analysis
- Each country’s data is modeled separately. Inconsistent or incomplete data, such as zero or missing values, are handled:
  - Countries with significant missing or null data (e.g., Czechia, Lithuania) are excluded.
  - In some cases (e.g., Hungary, Ireland), initial rows with zeros are removed before analysis.

### Visualization
- The SIR model outputs the trajectories for susceptible (\(S\)), infected (\(I\)), and recovered (\(R\)) populations.
- Results are plotted and saved as PNG images for each country.

---

## Code Overview

### Workflow
1. **Loading the data**:
   - COVID-19 data for EU/EEA countries from ECDC in CSV format.
   - Parameters (\( \beta \) and \( \gamma \)) are saved to and loaded from a JSON file.

2. **Data Cleaning**:
   - Handling missing values, empty rows, and inconsistent data per country.

3. **Fitting the SIR model**:
   - Estimation of \( \beta \) and \( \gamma \) using least squares fitting to active infection data.

4. **Model Simulation**:
   - Numerical integration of SIR equations using `scipy.integrate.odeint`.

5. **Visualization**:
   - Graphical representation of \( S \), \( I \), and \( R \) trends over time.
   - Graphs are saved locally for review.

---

## Requirements
- Python 3.7+
- Libraries:
  ```bash
  pip install pandas numpy matplotlib scipy
  ```

---

## How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/sir-model.git
   cd sir-model
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Replace the placeholder paths with your dataset's path:
   ```python
   data = pd.read_csv('/path/to/data_covid-19_EU.csv')
   ```

4. Execute the script:
   ```bash
   python sir_model.py
   ```

5. Output:
   - Graphs for \( S \), \( I \), and \( R \) saved as PNG files in the working directory.
   - Estimated \( \beta \) and \( \gamma \) values saved in `params.json`.

---

## Key Considerations

### Data Quality
- Countries with insufficient or null data (e.g., zero cases and deaths) are excluded from analysis.
- Recovery period is assumed to be **14 days**.

### Model Limitations
- This basic SIR model does not account for vaccination, reinfections, or other external interventions.

---

## Acknowledgments
Data was sourced from the **European Centre for Disease Prevention and Control (ECDC)** and spans 2020–2022. Recovery period assumptions follow WHO guidelines for COVID-19 symptom duration.

---
