import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics

"""
TODO:
- requirements.txt
- Put conclusions printed into Readme
- Try to improve inputs:
    - TODOs in preprocessing
    - Think how to take the person's uniqueness into account
    - Education split as per TODO there
    - Month split categorically (or winter/summer etc.)
    - Day of week (separate into beg week, mid week, end week)
    - Age - split into groups?
- 
"""


INPUT_FILE = "outputs/Absenteeism_preprocessed_mine.csv"
TEST_FRACTION = 0.2


def prepare_data(scale_dummies=False, features_to_remove=None):
    pd.options.display.max_columns = None
    pd.options.display.max_rows = None
    np.set_printoptions(formatter={'float': lambda x: "{0:0.2f}".format(x)}, linewidth=120)

    df = pd.read_csv(INPUT_FILE)
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
        df_inputs_for_scaling = df_inputs_for_scaling.drop(['Reason_1', 'Reason_2', 'Reason_3', 'Reason_4', 'Education'], axis=1)

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
    print(f'score of training: {round(score, 2)}')

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


inputs, targets, features = prepare_data(scale_dummies=False,
                                         features_to_remove=
                                         ['Day of the Week', 'Distance to Work', 'Daily Work Load Average'])
single_model(inputs, targets, features)




