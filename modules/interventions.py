def suggest_interventions(df):
    intervention_map = {
        0: "Low Risk: Maintain current wellness routine",
        1: "Medium Risk: Recommend ergonomic workshops and health checks",
        2: "High Risk: Immediate medical attention and personalized coaching"
    }
    df['intervention'] = df['risk_group'].map(intervention_map)
    return df
