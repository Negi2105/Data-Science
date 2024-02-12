#Question 2, 3, 4(a)
try:   
    import pandas as pd
    import matplotlib.pyplot as plt

    df = pd.read_excel("stuntung_sanitation.xlsx")
    data = pd.read_excel("stuntung_sanitation.xlsx", sheet_name="Data Definition")
    
    selected_columns = ['a6', 'cageg', 'fidg', 'b10', 'd1', 'd6', 'e3', 'e4', 'stunting']
    selected_columns = sorted(selected_columns)

    data_types = []
    definitions = []

    for col_name in selected_columns:
        if col_name in df.columns:
            col_dtype = df[col_name].dtype
            data_types.append("Numeric" if col_dtype in ['int64', 'float64'] else "Ordinal" if col_dtype == 'object' else "Unknown")

    for col_name in selected_columns:
        matching_row = data[data.iloc[:, 0] == col_name].iloc[0, 1]
        definitions.append(matching_row)

    output_data = {'Code': selected_columns, 'Definition': definitions, 'Data Type': data_types}
    result_df = pd.DataFrame(output_data)
    print(result_df)


    count_df=df.isnull().sum().sum()                
    print(f"The NULL values in dataset are: {count_df}")              
    for i in data.iterrows():
        if i[1][0] == 'd1':
            x = i[1]
    d1_mapping = dict(zip(x[::2], x[1::2]))

    label_counts = df['d1'].value_counts()
    percentage_counts = (label_counts / label_counts.sum()) * 100

    selected_labels = [d1_mapping[label] for label, percent in percentage_counts.items() if percent > 4 and label in d1_mapping]
    for i in range(len(df['d1'].value_counts())-len(selected_labels)):
        selected_labels.append("")
    plt.figure(figsize=(8,8))
    plt.pie(df['d1'].value_counts(), labels=selected_labels, autopct=lambda p: f'{p:.1f}%' if p > 4 else '')
    plt.legend(loc="lower left", bbox_to_anchor=(1, 0.5), prop={'size': 6})
    plt.title("Proportions of the main sources of Drinking Water ")
    plt.show()
except FileNotFoundError:
    raise FileNotFoundError

#Question 4(b)

try:
    import pandas as pd
    import matplotlib.pyplot as plt

    df = pd.read_excel("stuntung_sanitation.xlsx")
    data = pd.read_excel("stuntung_sanitation.xlsx", sheet_name="Data Definition")

    a = []
    y = []
    dic = {}
    count_d6 = df['d6'].count()

    for i in data.iterrows():
        if i[1][0] == 'd6':
            x = i[1]

    for i in range(2, len(x), 2):
        dic[x[i]] = x[i + 1]

    b = list(df['d6'].value_counts())
    p = []

    for i in df['d6'].value_counts():
        p.append((i / count_d6) * 100)

    for i in dic.keys():
        if pd.notna(i):
            y.append(str(i))

    sort = [dic[key] for key in df['d6'].value_counts().index]
    for i in sort:
        if pd.notna(i):
            a.append(str(i)) 

    fig, ax = plt.subplots()
    bars = plt.bar(a, b)
    for bar, percentage in zip(bars, p):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height, f'{percentage:.1f}%', ha='center', va='bottom')
    plt.title("Distribution of Toilet facility Types")
    plt.xticks(rotation=45)
    plt.ylabel("Count")
    plt.show()
except FileNotFoundError:
    raise FileNotFoundError

#Question 5 (a)

try:
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    from scipy.stats import sem
    from scipy.stats import chi2_contingency

    df = pd.read_excel("stuntung_sanitation.xlsx")
    data = pd.read_excel("stuntung_sanitation.xlsx", sheet_name="Data Definition")

    a = []
    for i in data.iterrows():
        if i[1][0] == 'fidg':
            x = i[1]

    fidg_mapping = dict(zip(x[::2], x[1::2]))

    for key, value in fidg_mapping.items():
        if pd.notna(value):
            a.append(value)

    print("Null Hypothesis: There is no association between childhood stunting and family income. \n")
    print("Alternate Hypothesis: There is an association between childhood stunting and family income.\n")

    alpha=0.05
    contingency_table = pd.crosstab(df['stunting'], df['fidg'])
    chi2, p, _, _ = chi2_contingency(contingency_table)

    print(f"Chi-square statistic: {chi2}")
    print(f"P-value: {p}")

    if p < alpha:
        print("Reject the null hypothesis. There is an association between childhood stunting and family income.")
    else:
        print("Fail to reject the null hypothesis. There is no association between childhood stunting and family income.")

    stunting_rates = df.groupby('fidg')['stunting'].mean()
    standard_errors = df.groupby('fidg')['stunting'].sem()
    plt.figure(figsize=(8, 6))
    ax = sns.barplot(x=stunting_rates.index, y=stunting_rates.values, errorbar='sd', yerr=standard_errors, palette='viridis')

    for i, (value, err) in enumerate(zip(stunting_rates, standard_errors)):
        ax.text(i, value + 0.02, f'{value*100:.1f}% ± {err*100:.1f}%', ha='center', va='bottom')

    plt.title('Childhood Stunting Rates by Family Income')
    plt.xlabel('Family Monthly Income')
    plt.ylabel('Proportion of Childhood Stunting')
    plt.xticks(ticks=range(len(a[1:])), labels=a[1:])
    plt.show()
except FileNotFoundError:
    raise FileNotFoundError

#Question 5(b)

try:
    import pandas as pd
    from scipy.stats import chi2_contingency
    import matplotlib.pyplot as plt
    import seaborn as sns

    print("Null Hypothesis: There is no association between fulfilling minimum dietary diversity and stunting.")
    print("Alternate Hypothesis: There is an association between fulfilling minimum dietary diversity and stunting.\n")

    alpha=0.05
    contingency_table = pd.crosstab(df['e4'], df['stunting'])

    chi2, p, _, _ = chi2_contingency(contingency_table)

    print(f"Chi-square statistic: {chi2}")
    print(f"P-value: {p}")

    if p < alpha:
        print("Reject the null hypothesis. There is an association between fulfilling minimum dietary diversity and stunting.")
    else:
        print("Fail to reject the null hypothesis. There is no association between fulfilling minimum dietary diversity and stunting.\n")

    stunting_rates = df.groupby('e4')['stunting'].mean()
    standard_errors = df.groupby('e4')['stunting'].sem()

    plt.figure(figsize=(8, 6))
    ax = sns.barplot(x=stunting_rates.index, y=stunting_rates.values, errorbar='sd', yerr=standard_errors, palette='viridis')

    for i, (value, err) in enumerate(zip(stunting_rates, standard_errors)):
        ax.text(i, value + 0.02, f'{value*100:.1f}% ± {err*100:.1f}%', ha='center', va='bottom')

    print("----------------------------------------------------------")
    print("The rejection of the null hypothesis, indicating an association between fulfilling minimum dietary diversity and childhood stunting, aligns with the abstract's suggestion that there is an association between these factors. This consistency between the study's findings and the information presented in the abstract supports the abstract's claims regarding the relationship between minimum dietary diversity and childhood stunting.")

    plt.title('Stunting Proportion by Minimum Dietary Diversity')
    plt.xlabel('Minimum Dietary Diversity Fulfillment')
    plt.ylabel('Proportion of Stunting')
    plt.show()
except FileNotFoundError:
    raise FileNotFoundError

#Question 5(c)

import pandas as pd
from scipy.stats import chi2_contingency

alpha=0.05
contingency_table = pd.crosstab(df['d6'], df['stunting'])

chi2, p, _, _ = chi2_contingency(contingency_table)
print("Null Hypothesis: \n There is no association between the type of toilet and stunting. The distribution of stunting is the same across different types of toilets.\n") 
print("Alternative Hypothesis: There is an association between the type of toilet and stunting. The distribution of stunting is different across different types of toilets.\n")
print("--------\n")
print("When the dependent variable (in this case, stunting) is binary, and the independent variable is categorical, a chi-square test for independence will be used to assess whether there is an association between the two variables.")
print("---------\n")
print(f"Chi-square statistic: {chi2}")
print(f"P-value: {p} \n")
print("----------------------------------------")
if p<alpha:
    print("Reject the Null Hypothesis. There is an association between the type of toilet and stunting. The distribution of stunting is different across different types of toilets.\n")
else:
    print("Fail to reject the Null Hypothesis. There is no association between the type of toilet and stunting. The distribution of stunting is the same across different types of toilets.\n")
print("--------------------------------------------")
print("1-way ANOVA is typically used when the dependent variable is continuous, and you want to compare means across different levels of a categorical independent variable. Since stunting is binary in your case (0 or 1), a chi-square test for independence is more appropriate for assessing the association between stunting and the type of toilet.")
