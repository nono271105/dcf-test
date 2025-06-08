# 💸 Calculateur DCF Automatique

Bienvenue sur le **Calculateur DCF Automatique**, une application Streamlit intuitive permettant de réaliser une **valorisation par actualisation des flux de trésorerie** (Discounted Cash Flow – DCF).

🔗 **Application Web :** [https://dcf-auto.streamlit.app/](https://dcf-auto.streamlit.app/)

---

## 🎯 Objectif

Cet outil a été conçu pour estimer la valeur intrinsèque d'une entreprise à partir de ses flux de trésorerie futurs actualisés, selon une méthode rigoureuse inspirée des pratiques utilisées en banque d’investissement, private equity ou analyse financière.

Il fournit :

* Le **WACC** (coût moyen pondéré du capital)
* La **valeur d’entreprise (EV)**
* La **valeur des fonds propres (Equity Value)**
* Le **prix par action estimé**
* Le **détail des flux futurs actualisés et de la valeur terminale**

---

## 🧮 Fonctionnalités

* **Inputs paramétrables dynamiquement** via une barre latérale :

  * Données opérationnelles (EBIT, CapEx, D\&A…)
  * Structure du capital (Market Cap, dette, trésorerie…)
  * Hypothèses macroéconomiques (taux sans risque, bêta, croissance…)
* **Calcul automatique** du WACC selon le modèle MEDAF (CAPM)
* **Projection des FCFF** sur une période déterminée
* **Actualisation des flux et calcul de la valeur terminale**
* **Visualisation claire et pédagogique** des résultats et formules

---

## 📦 Structure du Projet

```bash
📁 dcf_auto
│
├── app.py               # Code principal Streamlit
├── requirements.txt     # Dépendances Python
└── README.md            # Ce fichier
```

---

## ▶️ Lancer l'application en local

### 1. Cloner le dépôt :

```bash
git clone https://github.com/ton-nom-utilisateur/dcf-auto.git
cd dcf-auto
```

### 2. Installer les dépendances :

```bash
pip install -r requirements.txt
```

### 3. Lancer l’application :

```bash
streamlit run app.py
```

---

## 🛠️ Technologies utilisées

* [Streamlit](https://streamlit.io/) — pour créer l’interface web interactive
* [Pandas](https://pandas.pydata.org/) — pour le traitement de données
* Python 3.9+

---

## 📊 Exemples d'utilisation

* Comparer une valorisation DCF à la valorisation actuelle du marché
* Tester différents scénarios de croissance
* Comprendre l’impact du WACC sur la valorisation
* Préparer un pitch, un entretien ou une présentation financière

---

## 📈 Résultat attendu

Une fois tous les paramètres renseignés, l’application vous renvoie :

* Le **prix théorique par action**
* Les valeurs de l'entreprise et des capitaux propres
* Une **explication détaillée des calculs** du WACC et de la valeur terminale
* Les **FCF futurs projetés et actualisés**

---

## 💬 Avertissement

> ⚠️ Ce calculateur est un outil pédagogique. Les résultats obtenus ne doivent **pas** être utilisés comme seule base de décision d’investissement. Il ne remplace en aucun cas une analyse complète ou le jugement d’un analyste financier.
