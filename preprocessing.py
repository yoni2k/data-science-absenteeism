import pandas as pd

"""
Goal: predict employee absence from work based on numerous factors.  
See input file "inputs/Absenteeism-data.csv" for different inputs and factors.
Also, see PREPROCESSING.md for analysis of inputs and decisions for preprocessing

TODO:
- Update requirements.txt
"""

INPUT_FILE = "inputs/Absenteeism-data.csv"
OUTPUT_FILE = "outputs/Absenteeism_preprocessed_mine.csv"

def preprocess():
    pd.options.display.max_columns = None
    pd.options.display.max_rows = None

    raw_data_df = pd.read_csv(INPUT_FILE)
    df = raw_data_df.copy()

    print(f'================ Original shape: {df.shape}, Head and describe: ')
    print(df.head().to_string())
    print(df.describe().to_string())
    print('---------- Frame info:')
    print(df.info())
    print('---------- Number unique:')
    print(df.nunique(axis=0))
    print(f'Number 0s in Absenteeism Time in Hours: {df[df["Absenteeism Time in Hours"]==0].shape[0]}')

    # ------------- ID
    # Dropping ID variable. Reason: we would like to predict not based on who the person is, but his characteristics
    df = df.drop(['ID'], axis=1)

    # ------------- Reason for Absence
    # Changing reason into a cetegorical value and categorize together. It's OK to drop first since it has 38/700 > 5% observations
    print('Reason for Absence - adding dummy variables - number of values of each category before dropping first value:')
    print(pd.get_dummies(df['Reason for Absence']).sum(axis=0))
    # TODO - understand why we are dropping first, and then categorizing, should have perhaps first categories, then dropped?
    reason_columns = pd.get_dummies(df['Reason for Absence'], drop_first=True)
    # reason_columns = pd.get_dummies(df['Reason for Absence'], prefix='R')
    df = df.drop(['Reason for Absence'], axis=1)
    print('============ Head of reasons dummy variables')
    print(reason_columns.head().to_string())

    # Split reasons into 4 categories (pre-provided in the course based on analysis):
    #   1-14, 15-17, 18-21, 22-end
    reason_type_1 = reason_columns.loc[:, 1:14].sum(axis=1)
    reason_type_2 = reason_columns.loc[:, 15:17].sum(axis=1)
    reason_type_3 = reason_columns.loc[:, 18:21].sum(axis=1)
    reason_type_4 = reason_columns.loc[:, 22:].sum(axis=1)
    print("reason_type_1 head:\n" + reason_type_1.head().to_string())
    print("reason_type_2 head:\n" + reason_type_2.head().to_string())
    print("reason_type_3 head:\n" + reason_type_3.head().to_string())
    print("reason_type_4 head:\n" + reason_type_4.head().to_string())

    df_reasons = pd.concat([reason_type_1, reason_type_2, reason_type_3, reason_type_4], axis=1)
    df_reasons.columns = ['Reason_1', 'Reason_2', 'Reason_3', 'Reason_4']
    df = pd.concat([df_reasons, df], axis=1)
    print('============ Head of df after adding reasons')
    print(df.head().to_string())
    print(f'Sum of all reasons: {sum(df["Reason_1"]) + sum(df["Reason_2"]) + sum(df["Reason_3"]) + sum(df["Reason_4"])}')

    # ------------- Date
    # Remove only month and day of week values, since we presume that's what might affect the absenteeism
    # TODO - what are we doing with dates - this format is probably better, but still not the best?
    print(f"Type of date field: {type(df['Date'][0])}")
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
    print(f'================ After performing date converstion, shape: {df.shape}, Head: ')
    print(df.head().to_string())
    print(f"Date - min: {min(df['Date'])}, max: {max(df['Date'])}, unique: {df['Date'].unique().shape}, null: {df['Date'].isnull().sum()}")

    df['Month Value'] = pd.DatetimeIndex(df['Date']).month
    df['Day of the Week'] = pd.DatetimeIndex(df['Date']).dayofweek
    df = df.drop(['Date'], axis=1)
    # reorder columns
    df = df[['Reason_1', 'Reason_2', 'Reason_3', 'Reason_4', 'Month Value', 'Day of the Week',
             'Transportation Expense', 'Distance to Work', 'Age', 'Daily Work Load Average', 'Body Mass Index',
             'Education', 'Children', 'Pets', 'Absenteeism Time in Hours']]
    print(f'================ After extracting relevant date fields, shape: {df.shape}, Head: ')
    print(df.head().to_string())

    # ------------- Education
    # Since there are very few non-1's, combine the rest together
    print(f'frequency of educations:\n{df["Education"].value_counts()}')
    df['Education'] = df['Education'].map({1:0, 2:1, 3:1, 4:1})
    print(f'frequency of educations after turning into 0 and 1:\n{df["Education"].value_counts()}')
    print(f'================ After turning education into dummies, shape: {df.shape}, Head: ')
    print(df.head().to_string())

    # TODO - consider having 3 categories (combining just 3 & 4 as below)
    """
    education_columns = pd.get_dummies(df["Education"], drop_first=True)
    education_columns.columns = ['Ed_2', 'Ed_3', 'Ed_4']
    print(f'================ Education dummies, shape: {education_columns.shape}, Head: ')
    print(education_columns.head(10).to_string())
    education_columns['Ed_3_4'] = education_columns['Ed_3'] + education_columns['Ed_4']
    education_columns = education_columns.drop(['Ed_3', 'Ed_4'], axis=1)
    print(f'================ Education dummies after combining Education 3 and 4, shape: {education_columns.shape}, Head: ')
    print(education_columns.head(10).to_string())

    df = df.drop(['Education'], axis=1)
    df = pd.concat([df, education_columns], axis=1)
    df = df[['Reason_1', 'Reason_2', 'Reason_3', 'Reason_4', 'Month Value', 'Day of the Week', 'Transportation Expense',
             'Distance to Work', 'Age', 'Daily Work Load Average', 'Body Mass Index', 'Ed_2', 'Ed_3_4',
             'Children', 'Pets', 'Absenteeism Time in Hours']]
    print(df.columns.values)
    print(f'================ After turning education into dummies, shape: {df.shape}, Head: ')
    print(df.head().to_string())
    """

    # For some reason, even though the input round column 'Daily Work Load Average' rounded to 3 places, in output
    #  some values are with many more places, so rounded it
    df['Daily Work Load Average'] = round(df['Daily Work Load Average'], 3)

    print(f'================ After resetting index, shape: {df.shape}, Head: ')
    print(df.head().to_string())
    df.to_csv(OUTPUT_FILE, index=False)


preprocess()