import matplotlib.pyplot as plt

def summary_report(df):
    counts = df['risk_group'].value_counts().sort_index()
    plt.bar(['Low', 'Medium', 'High'], counts)
    plt.title("Employees by Risk Group")
    plt.xlabel("Risk Group")
    plt.ylabel("Number of Employees")
    plt.savefig("risk_summary.png")
    plt.show()
