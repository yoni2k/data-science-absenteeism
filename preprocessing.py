import pandas as pd

"""
Goal: predict employee absence from work based on numerous factors.  
See input file "inputs/Absenteeism-data.csv" for different inputs and factors.
Also, see PREPROCESSING.md for analysis of inputs and decisions for preprocessing
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
    # Not taking ID column. Reason: we would like to predict not based on who the person is, but his characteristics

    # ------------- Reason for Absence
    # Changing reason into a cetegorical value and categorize together.
    #   It's OK to drop first since it has 38/700 > 5% observations
    print('Reasons for Absence - adding dummy variables - number of values of each category before dropping first value:')
    print(df['Reason for Absence'].value_counts())
    # TODO - understand why we are dropping first, and then categorizing,
    #  should have perhaps first categories, then dropped?
    reason_columns = pd.get_dummies(df['Reason for Absence'], drop_first=True)
    print('============ Head of reasons dummy variables')
    print(reason_columns.head().to_string())

    # Split reasons into 4 categories (pre-provided in the course based on analysis):
    #   1-14, 15-17, 18-21, 22-end
    reason_type_1 = reason_columns.loc[:, 1:14].sum(axis=1)
    reason_type_2 = reason_columns.loc[:, 15:17].sum(axis=1)
    reason_type_3 = reason_columns.loc[:, 18:21].sum(axis=1)
    reason_type_4 = reason_columns.loc[:, 22:].sum(axis=1)
    print(f'Sum of all reasons: {sum(reason_type_1) + sum(reason_type_2) + sum(reason_type_3) + sum(reason_type_4)}')

    df_preprocessed = pd.concat([reason_type_1, reason_type_2, reason_type_3, reason_type_4], axis=1)
    df_preprocessed.columns = ['Reason_1', 'Reason_2', 'Reason_3', 'Reason_4']
    print('============ Head of df_preprocessed after adding reasons')
    print(df_preprocessed.head().to_string())

    # ------------- Date
    # Remove only month and day of week values, since we presume that's what might affect the absenteeism
    # Change to datetime64 format
    print(f"Type of date field: {type(df['Date'][0])}")
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
    print(f'================ After performing date conversion, shape: {df.shape}, Head: ')
    print(df.head().to_string())
    print(f"Date - min: {min(df['Date'])}, max: {max(df['Date'])}, unique: {df['Date'].unique().shape}, null: {df['Date'].isnull().sum()}")

    df_preprocessed['Month Value'] = pd.DatetimeIndex(df['Date']).month
    df_preprocessed['Day of the Week'] = pd.DatetimeIndex(df['Date']).dayofweek
    print(f'================ After adding month and day of week fields, shape: {df_preprocessed.shape}, Head: ')
    print(df_preprocessed.head().to_string())

    # Take the following as is:
    #  'Transportation Expense','Distance to Work', 'Age', 'Daily Work Load Average', 'Body Mass Index'
    df_preprocessed['Transportation Expense'] = df['Transportation Expense']
    df_preprocessed['Distance to Work'] = df['Distance to Work']
    df_preprocessed['Age'] = df['Age']
    df_preprocessed['Daily Work Load Average'] = df['Daily Work Load Average']
    df_preprocessed['Body Mass Index'] = df['Body Mass Index']
    print(f"================ After adding 'Transportation Expense','Distance to Work', 'Age', 'Daily Work Load Average',"
          f" 'Body Mass Index', shape: {df_preprocessed.shape}, Head: ")
    print(df_preprocessed.head().to_string())

    # ------------- Education
    # Since there are very few non-1's, combine the rest together
    # TODO - consider having 3 categories (combining just 3 & 4 and not 1,2,3 together),
    #   since 4th category is the only one that's really small
    #   Then according to the course, need to add dummy values - turn from categorical
    print(f'frequency of educations:\n{df["Education"].value_counts()}')
    df_preprocessed['Education'] = df['Education'].map({1: 0, 2: 1, 3: 1, 4: 1})
    print(f'frequency of educations after turning into 0 and 1:\n{df_preprocessed["Education"].value_counts()}')
    print(f'================ After turning education into dummies, shape: {df_preprocessed.shape}, Head: ')
    print(df_preprocessed.head().to_string())

    # Adding as is 'Children', 'Pets', 'Absenteeism Time in Hours'
    df_preprocessed['Children'] = df['Children']
    df_preprocessed['Pets'] = df['Pets']
    df_preprocessed['Absenteeism Time in Hours'] = df['Absenteeism Time in Hours']
    print(f"================ After adding 'Children', 'Pets', 'Absenteeism Time in Hours' - final version, "
          f"shape: {df_preprocessed.shape}, Head: ")
    print(df_preprocessed.head().to_string())

    # For some reason, even though the input round column 'Daily Work Load Average' rounded to 3 places, in output
    #  some values are with many more places, so rounded it
    df_preprocessed['Daily Work Load Average'] = round(df_preprocessed['Daily Work Load Average'], 3)

    # Write out to a csv file for future use
    df_preprocessed.to_csv(OUTPUT_FILE, index=False)


preprocess()