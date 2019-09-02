import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics

"""
Goal: predict employee absence from work based on numerous factors.  
See input file "inputs/Absenteeism-data.csv" for different inputs and factors.
Also, see DETAILED_STEPS.md for analysis of inputs and decisions for preprocessing

TODO:
- requirements.txt
- Put conclusions printed into Readme
- Move file of OUTPUT to inputs or general files
- Try to improve inputs:
    - TODOs in preprocessing
    - Think how to take the person's uniqueness into account
    - Education split as per TODO there
    - Month split categorically (or winter/summer etc.)
    - Day of week (separate into beg week, mid week, end week)
    - Age - split into groups?
"""

TEST_FRACTION = 0.2
ORIG_INPUT_FILE = "files/Absenteeism-data.csv"
PREPROCESSED_FILE = "files/Absenteeism_preprocessed_mine.csv"


def preprocess():
    pd.options.display.max_columns = None
    pd.options.display.max_rows = None

    raw_data_df = pd.read_csv(ORIG_INPUT_FILE)
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

    # ------------- Date
    # Remove only month and day of week values, since we presume that's what might affect the absenteeism
    # Change to datetime64 format
    print(f"Type of date field: {type(df['Date'][0])}")
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
    print(f'================ After performing date conversion, shape: {df.shape}, Head: ')
    print(df.head().to_string())
    print(f"Date - min: {min(df['Date'])}, max: {max(df['Date'])}, unique: {df['Date'].unique().shape}, "
          f"null: {df['Date'].isnull().sum()}")

    months = pd.get_dummies(pd.DatetimeIndex(df['Date']).month, prefix="Month")
    print(f'Frequences of months:\n{pd.DatetimeIndex(df["Date"]).month.value_counts()}')
    months['July_Aug'] = months['Month_7'] + months['Month_8']
    df_preprocessed = months['July_Aug']

    print(f'================ After adding month, shape: {df_preprocessed.shape}, Head: ')
    print(df_preprocessed.head().to_string())

    days_of_week = pd.DatetimeIndex(df['Date']).dayofweek.map({0:0, 1:1, 2:2, 3:3, 4:4, 5:0, 6:0})
    print(f'Value counts of Day of Week:\n{pd.DatetimeIndex(df["Date"]).dayofweek.value_counts()}')
    print(f'Value counts of Day of Week after putting Saturday, Sunday as Monday:\n{days_of_week.value_counts()}')
    days_of_week = pd.get_dummies(days_of_week)
    days_of_week.columns = ['Day_Mon', 'Day_Tue', 'Day_Wed', 'Day_Thu', 'Day_Fri']
    days_of_week = days_of_week.drop(['Day_Tue', 'Day_Wed', 'Day_Thu', 'Day_Fri'], axis=1)
    df_preprocessed = pd.concat([df_preprocessed, days_of_week], axis=1)
    print(f'================ After adding day of week, shape: {df_preprocessed.shape}, Head:\n'
          f'{df_preprocessed.head().to_string()}')

    """
    df_preprocessed['Day of the Week'] = pd.DatetimeIndex(df['Date']).dayofweek
    print(f'================ After adding month and day of week fields, shape: {df_preprocessed.shape}, Head: ')
    print(df_preprocessed.head().to_string())
    """

    # Take the following as is: 'Transportation Expense','Distance to Work'
    df_preprocessed['Transportation Expense'] = df['Transportation Expense']
    df_preprocessed['Distance to Work'] = df['Distance to Work']

    print(f"================ After adding 'Transportation Expense','Distance to Work', "
          f"shape: {df_preprocessed.shape}, Head:\n{df_preprocessed.head().to_string()}")

    print(f"Age frequencies:\n{df['Age'].value_counts()}")
    print(f'Age histogram: {np.histogram(df["Age"], bins=5)}')
    print(f"bincount of ages: 30, 35, 38, 41: {np.bincount(np.digitize(df['Age'], np.array([30, 35, 38, 41])))}")

    ages_ranges = pd.cut(df['Age'], bins=6, precision=0, labels=False)
    print(pd.cut(df['Age'], bins=6, precision=0))
    ages_ranges = ages_ranges.map({0: 0, 1: 1, 2: 2, 3: 3, 4: 3})
    print(f"Age frequencies:\n{ages_ranges.value_counts()}")
    ages_columns = pd.get_dummies(ages_ranges)
    ages_columns.columns = ['Age_28_33', 'Age_34_39', 'Age_40_46', 'Age_47_58']
    ages_columns = ages_columns.drop(['Age_28_33', 'Age_47_58'], axis=1)
    df_preprocessed = pd.concat([df_preprocessed, ages_columns], axis=1)
    print(f"================ After adding 'Age' as categorical variables, shape: {df_preprocessed.shape}, Head: ")
    print(df_preprocessed.head().to_string())

    # Take the following as is: 'Daily Work Load Average','Body Mass Index'
    df_preprocessed['Daily Work Load Average'] = df['Daily Work Load Average']
    df_preprocessed['Body Mass Index'] = df['Body Mass Index']
    print(f"================ After adding 'Daily Work Load Average','Body Mass Index', "
          f"shape: {df_preprocessed.shape}, Head:\n{df_preprocessed.head().to_string()}")

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
    df_preprocessed.to_csv(PREPROCESSED_FILE, index=False)


def prepare_data(scale_dummies=False, features_to_remove=None):
    pd.options.display.max_columns = None
    pd.options.display.max_rows = None
    np.set_printoptions(formatter={'float': lambda x: "{0:0.2f}".format(x)}, linewidth=120)

    df = pd.read_csv(PREPROCESSED_FILE)
    print(f"Read data, shape: {df.shape}, head:\n{df.head().to_string()}")

    if features_to_remove:
        df = df.drop(features_to_remove, axis=1)
        print(f"After dropping features data, shape: {df.shape}, head:\n{df.head().to_string()}")

    # Taking the mean / median as a cutoff point, which will also make our targets balanced
    mean_of_absense_hours = df['Absenteeism Time in Hours'].median()
    df['Excessive Absenteeism'] = df['Absenteeism Time in Hours'].apply(lambda x: 1 if x > mean_of_absense_hours else 0)
    df = df.drop(['Absenteeism Time in Hours'], axis=1)
    print("After adding Excessive Absenteeism, absent above average:\n" + df.head().to_string())

    # scale the data, prepare inputs
    df_inputs_for_scaling = df.drop(['Excessive Absenteeism'], axis=1)
    if not scale_dummies:
        df_inputs_for_scaling = df_inputs_for_scaling.drop(
            ['Age_34_39', 'Age_40_46', 'Day_Mon', 'July_Aug'], axis=1)

    columns_to_scale = df_inputs_for_scaling.columns.values

    scaler = StandardScaler()
    scaler.fit(df_inputs_for_scaling)  # just calculates and saves Means and STDs
    df[columns_to_scale] = scaler.transform(df_inputs_for_scaling)
    print(f"Data after scaling, shape: {df.shape}, head:\n{df.head().to_string()}")
    scaled_inputs = df.iloc[:, :-1].to_numpy()
    print(f'inputs shape: {scaled_inputs.shape}, first 5 lines:\n{scaled_inputs[:5, :]}')

    # prepare targets
    unshuffled_targets = df['Excessive Absenteeism'].to_numpy()
    print(f'targets shape: {unshuffled_targets.shape}, first 5 lines:{unshuffled_targets[:5]}')

    return scaled_inputs, unshuffled_targets, df.columns.values[:-1]


def shuffle_split_train_test(inputs, targets):
    # shuffling and splitting into test and train
    # TODO - make random state an input parameter
    x_train, x_test, y_train, y_test = train_test_split(
        inputs, targets, test_size=TEST_FRACTION, random_state=20)
    print(f"shapes of split data - input_train: {x_train.shape}, inputs_test: {x_test.shape}, "
          f"targets_train: {y_train.shape}, targets_test: {y_test.shape}")
    return x_train, x_test, y_train, y_test


def single_model(inputs, targets, features):
    x_train, x_test, y_train, y_test = shuffle_split_train_test(inputs, targets)

    reg = LogisticRegression()
    reg.fit(x_train, y_train)

    score = reg.score(x_train, y_train)
    print(f'score of training: {round(score, 3)}')

    # manually calculate score
    y_pred = reg.predict(x_train)
    y_diff = abs(y_train - y_pred)
    num_diff = sum(y_diff)
    num_same = y_diff.shape[0] - num_diff
    print(f'type y_diff: {type(y_diff)}, num_diff: {num_diff}, num_same: {num_same}, num total: {y_diff.shape[0]}, '
          f'fraction same: {round(num_same/y_diff.shape[0], 2)}')

    # get and print intercept and coefficients
    df1 = pd.DataFrame({'Features': ['Intercept'], 'Coefs': reg.intercept_})
    df2 = pd.DataFrame({'Features': features, 'Coefs': reg.coef_[0]})
    df = df1.append(df2)
    df = df.reset_index(drop=True)
    df['Odds_ratio'] = np.exp(df['Coefs'])
    print(f'Intercept and coefficients:\n{df.to_string()}')
    print(f'Intercept and coefficients sorted:\n{df.sort_values("Odds_ratio", axis=0).to_string()}')

    # test
    test_score = reg.score(x_test, y_test)
    print(f'score of testing: {round(test_score, 3)}')


def main():
    preprocess()
    inputs, targets, features = prepare_data(scale_dummies=False,
                                             features_to_remove=['Distance to Work', 'Education',
                                                                 'Body Mass Index'])
    single_model(inputs, targets, features)


main()
