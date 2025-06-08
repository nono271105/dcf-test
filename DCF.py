import streamlit as st
import pandas as pd

# --- Configuration de la page Streamlit ---
st.set_page_config(
    page_title="Calculateur DCF Automatique",
    page_icon="💸",
    layout="wide"
)

# --- Fonctions de calcul ---

def calculate_wacc(market_cap, total_debt, interest_expense, tax_rate, risk_free_rate, beta, market_return):
    """Calcule le Coût Moyen Pondéré du Capital (WACC)."""
    # Valeur totale de l'entreprise (E + D)
    total_value = market_cap + total_debt
    if total_value == 0:
        return 0, 0, 0

    # Pondérations
    weight_equity = market_cap / total_value
    weight_debt = total_debt / total_value

    # Coût des fonds propres (Equity) via le CAPM / MEDAF
    cost_of_equity = risk_free_rate + beta * (market_return - risk_free_rate)

    # Coût de la dette (Debt)
    cost_of_debt = interest_expense / total_debt if total_debt > 0 else 0
    
    # Formule du WACC
    wacc = (weight_equity * cost_of_equity) + (weight_debt * cost_of_debt * (1 - tax_rate))
    
    return wacc, cost_of_equity, cost_of_debt

def calculate_dcf(ebit, tax_rate, da, capex, delta_nwc,
                  wacc, forecast_period, short_term_growth, perpetual_growth,
                  total_debt, cash, shares_outstanding):
    """Calcule le DCF et le prix de l'action qui en résulte."""
    # Calcul du Free Cash Flow to Firm (FCFF) de l'année 0
    nopat = ebit * (1 - tax_rate)
    fcff_initial = nopat + da - capex - delta_nwc

    # Projection des FCFF futurs
    projected_fcffs = []
    for year in range(1, forecast_period + 1):
        fcff = fcff_initial * ((1 + short_term_growth) ** year)
        projected_fcffs.append(fcff)

    # Calcul de la Valeur Terminale (Terminal Value) via Gordon-Shapiro
    last_projected_fcff = projected_fcffs[-1]
    terminal_value = (last_projected_fcff * (1 + perpetual_growth)) / (wacc - perpetual_growth)

    # Actualisation des flux de trésorerie
    discounted_fcffs = [fcff / ((1 + wacc) ** (year + 1)) for year, fcff in enumerate(projected_fcffs)]
    pv_terminal_value = terminal_value / ((1 + wacc) ** forecast_period)

    # Calcul de la Valeur d'Entreprise (Enterprise Value)
    enterprise_value = sum(discounted_fcffs) + pv_terminal_value
    
    # Calcul de la Valeur des Fonds Propres (Equity Value)
    equity_value = enterprise_value - total_debt + cash
    
    # Calcul du prix de l'action
    share_price = equity_value / shares_outstanding if shares_outstanding > 0 else 0
    
    return share_price, enterprise_value, equity_value, projected_fcffs, terminal_value

# --- Interface Utilisateur (Sidebar pour les inputs) ---

st.sidebar.header("PARAMÈTRES DU DCF 📊")

st.sidebar.subheader("Données de l'entreprise (Année 0)")
ebit = st.sidebar.number_input("EBIT (Bénéfice avant intérêts et impôts)", value=500.0)
da = st.sidebar.number_input("Dépréciation & Amortissement (D&A)", value=80.0)
capex = st.sidebar.number_input("Dépenses d'investissement (CapEx)", value=120.0)
delta_nwc = st.sidebar.number_input("Variation du Besoin en Fonds de Roulement (ΔNWC)", value=30.0)
interest_expense = st.sidebar.number_input("Charges d'intérêts", value=40.0)

st.sidebar.subheader("Structure du Capital et Actions")
market_cap = st.sidebar.number_input("Capitalisation Boursière (Market Cap)", value=4000.0)
total_debt = st.sidebar.number_input("Dette Totale", value=1000.0)
cash = st.sidebar.number_input("Trésorerie et équivalents (Cash)", value=200.0)
shares_outstanding = st.sidebar.number_input("Nombre d'actions en circulation", value=100.0)

st.sidebar.subheader("Hypothèses de Marché et de Croissance")
tax_rate = st.sidebar.slider("Taux d'imposition (%)", 0, 50, 25) / 100.0
risk_free_rate = st.sidebar.slider("Taux sans risque (%)", 0.0, 10.0, 3.0) / 100.0
market_return = st.sidebar.slider("Rendement attendu du marché (%)", 5.0, 15.0, 8.0) / 100.0
beta = st.sidebar.slider("Bêta de l'action (β)", 0.5, 2.5, 1.2)
forecast_period = st.sidebar.slider("Période de prévision explicite (années)", 3, 10, 5)
short_term_growth = st.sidebar.slider("Taux de croissance des FCF à court terme (%)", 0.0, 20.0, 5.0) / 100.0
perpetual_growth = st.sidebar.slider("Taux de croissance perpétuelle (%)", 0.0, 5.0, 2.0) / 100.0


# --- Affichage Principal ---

st.title("💸 Calculateur de Valorisation par DCF")
st.write("""
Cet outil réalise une analyse de type **Discounted Cash Flow (DCF)** pour estimer la valeur intrinsèque 
d'une action. Modifiez les paramètres dans la barre latérale pour voir les résultats se mettre à jour en temps réel.
""")
st.info(f"Les montants sont supposés être en millions de la devise de votre choix (par ex: M€). Le résultat final sera par action.")


# --- Calculs et Affichage des Résultats ---

if st.sidebar.button("Lancer le Calcul du DCF"):

    # 1. Calcul du WACC
    wacc, cost_of_equity, cost_of_debt = calculate_wacc(
        market_cap, total_debt, interest_expense, tax_rate, risk_free_rate, beta, market_return
    )

    # Vérification pour éviter la division par zéro dans la formule de la valeur terminale
    if wacc <= perpetual_growth:
        st.error(f"Erreur Critique : Le WACC ({wacc:.2%}) doit être supérieur au taux de croissance perpétuel ({perpetual_growth:.2%}) pour que le calcul de la valeur terminale soit valide.")
    else:
        # 2. Calcul du DCF
        share_price, enterprise_value, equity_value, projected_fcffs, terminal_value = calculate_dcf(
            ebit, tax_rate, da, capex, delta_nwc, wacc, forecast_period, 
            short_term_growth, perpetual_growth, total_debt, cash, shares_outstanding
        )
        
        # --- Affichage des résultats ---
        st.header("Résultats de la Valorisation")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Prix de l'Action Estimé", f"{share_price:,.2f} €", delta=None, help="Prix par action calculé (Equity Value / Nb d'actions)")
        col2.metric("Valeur d'Entreprise (EV)", f"{enterprise_value:,.0f} M€", delta=None, help="Valeur totale de l'entreprise (dette + fonds propres)")
        col3.metric("Valeur des Fonds Propres", f"{equity_value:,.0f} M€", delta=None, help="Valeur revenant aux actionnaires (EV - Dette Nette)")

        st.markdown("---")

        # --- Détails des calculs intermédiaires ---
        with st.expander("🔍 Voir les détails des calculs intermédiaires"):
            
            st.subheader("Calcul du WACC (Coût Moyen Pondéré du Capital)")
            wacc_col1, wacc_col2, wacc_col3 = st.columns(3)
            wacc_col1.metric("Coût des Fonds Propres (Ke)", f"{cost_of_equity:.2%}")
            wacc_col2.metric("Coût de la Dette (Kd après impôt)", f"{cost_of_debt * (1 - tax_rate):.2%}")
            wacc_col3.metric("WACC", f"{wacc:.2%}", "Taux d'actualisation")
            
            st.latex(f'''
            WACC = \\frac{{E}}{{E+D}} \\times K_e + \\frac{{D}}{{E+D}} \\times K_d \\times (1 - TauxImpôt)
            ''')
            st.latex(f'''
            WACC = \\frac{{{market_cap:,.0f}}}{{{market_cap:,.0f}+{total_debt:,.0f}}} \\times {cost_of_equity:.2%} + \\frac{{{total_debt:,.0f}}}{{{market_cap:,.0f}+{total_debt:,.0f}}} \\times {cost_of_debt:.2%} \\times (1 - {tax_rate:.0%}) = \\bf{{{wacc:.2%}}}
            ''')
            
            st.subheader("Projection des Free Cash Flow (FCF)")
            fcff_data = {'Année': list(range(1, forecast_period + 1)), 'FCF Projeté': projected_fcffs}
            fcff_df = pd.DataFrame(fcff_data)
            fcff_df['FCF Actualisé'] = fcff_df.apply(lambda row: row['FCF Projeté'] / (1 + wacc)**row['Année'], axis=1)
            st.dataframe(fcff_df.style.format("{:,.2f}"))
            
            st.subheader("Calcul de la Valeur Terminale (TV)")
            pv_terminal_value = terminal_value / ((1 + wacc) ** forecast_period)
            st.write(f"La valeur terminale (représentant les flux au-delà de l'année {forecast_period}) est estimée à **{terminal_value:,.0f} M€**.")
            st.write(f"Sa valeur actuelle (actualisée à aujourd'hui) est de **{pv_terminal_value:,.0f} M€**.")

            st.subheader("Passage de la Valeur d'Entreprise à la Valeur par Action")
            st.code(f"""
            Valeur d'entreprise (Somme des FCF actualisés + PV de la TV) : {sum(fcff_df['FCF Actualisé']):,.0f} + {pv_terminal_value:,.0f} = {enterprise_value:,.0f} M€
            (-) Dette Totale                                                : -{total_debt:,.0f} M€
            (+) Trésorerie                                                  : +{cash:,.0f} M€
            = Valeur des Fonds Propres (Equity Value)                       : {equity_value:,.0f} M€
            
            (/) Nombre d'actions                                            : {shares_outstanding:,.0f}
            = PRIX DE L'ACTION ESTIMÉ                                       : {share_price:,.2f} €
            """, language=None)
else:
    st.info("Cliquez sur le bouton dans la barre latérale pour lancer le calcul après avoir ajusté les paramètres.")


st.markdown("---")
st.warning("""
**Avertissement :** Ce modèle est un outil éducatif et simplifié. Une véritable analyse DCF nécessite des recherches approfondies, des hypothèses justifiées et souvent plusieurs scénarios (optimiste, pessimiste, de base). Les résultats ne constituent en aucun cas un conseil en investissement.
""")