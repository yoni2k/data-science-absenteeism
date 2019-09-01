## Preprocessing
### Step 1 - learn, describe and decide on data 
#### General statistics:
- Types of received inputs:

        ID                           700 non-null int64
        Reason for Absence           700 non-null int64
        Date                         700 non-null object
        Transportation Expense       700 non-null int64
        Distance to Work             700 non-null int64
        Age                          700 non-null int64
        Daily Work Load Average      700 non-null float64
        Body Mass Index              700 non-null int64
        Education                    700 non-null int64
        Children                     700 non-null int64
        Pets                         700 non-null int64
        Absenteeism Time in Hours    700 non-null int64
#### Unique values per feature (out of 700 observations):
    ID                            34
    Reason for Absence            28
    Date                         432
    Transportation Expense        24
    Distance to Work              24
    Age                           21
    Daily Work Load Average       35
    Body Mass Index               16
    Education                      4
    Children                       5
    Pets                           6
    Absenteeism Time in Hours     19
- There are no null values (count = 700 for all columns, including date that doesn't appear in regular describe)
- ID - There are 34 unique IDs - possibly same workers that appear many times
    - **Decision**: Remove since we don't want to predict behavior of specific individual since Not sure it's a column we'll leave, but in any case it should not be a numeric data
- Reason for Absence
    - 28 unique values
    - **Decision**: Should not be treated like a number, but categorical data, categorize/group, add dummies. Course explained how makes sense to categorize in this case
- Date - There are 432 different dates out of 700 - possibly different times someone was absent
    - min: 2015-07-06, max: 2018-05-31 - almost 3 years
    - Has no nulls
    - **Decision**: take out relevant fields that might affect behavior: month and day of week
- Transportation expenses - Unique - 24, OK to have it as number
- Distance to work - 16 unique, OK to leave as number, although seems to be in whole units
- Age - 21 unique, OK to leave as number, although seems to be in whole units 
- Daily Work Load Average - OK to leave as number, not whole units
- Body Mass Index - 16 unique, OK to leave as number, whole numbers
- Education - 4 unique - whole numbers, seems to be a code, hopefully in meaningful order like 1 high school and higher.
    Frequencies:

        1    583
        3     73
        2     40
        4      4  
    - Assuming a higher number means higher education, could either leave as number or make categorical
    - **Decision**: follow what was done in the course - make categorical, group everything that's not high school education together because there are few like these
- Children - 5 unique - whole numbers, leave number
- Pets - 6 unique, min 0, max 8 - seems number of pets, whole numbers, leave number
- Absenteeism Time in Hours 
    - related to our target, number of **whole** hours missed starting this date (?) 
    - mean ~7, median 3, max 120
    - Has 39 '0' values - what does it mean 0.  If it's the person that wasn't missing, there should be many more like these.  **TBD** - Remove 0 values?
         

# Steps of Changes to the model:
## Step 1: Give an option not to standardize dummy variables for better interpretability
Especially to understand how Reasons effect the model exactly
### Values before removing standardizing dummies:
- Score: 0.78
- Intercept and coefficients sorted:

                       Features      Coefs   Odds_ratio 
    14                     Pets -0.333388    0.716492
    0                 Intercept -0.219576    0.802859
    9                       Age -0.200952    0.817952
    12                Education -0.135582    0.873207
    6           Day of the Week -0.070600    0.931834
    8          Distance to Work -0.039960    0.960828
    10  Daily Work Load Average -0.004624    0.995387
    5               Month Value  0.187823    1.206619
    11          Body Mass Index  0.319377    1.376270
    2                  Reason_2  0.334663    1.397470
    13                 Children  0.381681    1.464745
    7    Transportation Expense  0.706491    2.026866
    4                  Reason_4  1.327502    3.771610
    3                  Reason_3  1.560973    4.763455
    1                  Reason_1  2.074522    7.960741  
### Values after removing standardizing dummies
 - Score: 0.78
 - Intercept and coefficients sorted:
---
    Index               Features     Coefs    Odds_ratio
    0                 Intercept -1.470825    0.229736
    14                     Pets -0.285594    0.751567
    12                Education -0.230858    0.793852
    9                       Age -0.168624    0.844826
    6           Day of the Week -0.082573    0.920745
    8          Distance to Work -0.007418    0.992609
    10  Daily Work Load Average -0.003836    0.996172
    5               Month Value  0.161457    1.175221
    11          Body Mass Index  0.267500    1.306693
    13                 Children  0.355728    1.427219
    7    Transportation Expense  0.606960    1.834845
    4                  Reason_4  0.677719    1.969381
    2                  Reason_2  0.844320    2.326395
    1                  Reason_1  2.626143   13.820360
    3                  Reason_3  2.939719   18.910527
### Conclusions:
- Reasons given (vs. no reason given at all - reference category) is the strongest predictor
    - Reason 3 (Poisoning) is by far the strongest predictor
    - Reason 1 (Reguler sicknesses) is 2nd strongest predictor
    - Reason 2 (Pregnancy) affects somewhat
    - Reason 4 (Light deseases) affect a little
- Don't affect much and should be removed:
    - Day of the Week (although it would be interesting to put it as categorical data)
    - Distance to Work
    - Daily Work Load Average
    
## Step 2: Remove low coefficient features
- Remove:
    - Day of the Week
    - Distance to Work
    - Daily Work Load Average
- Score: 0.78 (up from previous 0.77 - so removing was helpful)
- Intercept and coefficients sorted:

                          Features     Coefs  Odds_ratio
        0                Intercept -1.465471    0.230969
        11                    Pets -0.277514    0.757665
        9                Education -0.234525    0.790946
        7                      Age -0.172451    0.841599
        5              Month Value  0.154937    1.167585
        8          Body Mass Index  0.275685    1.317433
        10                Children  0.342497    1.408460
        6   Transportation Expense  0.599798    1.821751
        4                 Reason_4  0.663907    1.942367
        2                 Reason_2  0.863386    2.371177
        1                 Reason_1  2.627499   13.839121
        3                 Reason_3  2.960507   19.307751
### Conclusions:
- All features are now significant, although the most significant are:
    - Reasons
    - Transportation expense
    - Children
    - BMI
    
## Improve model inputs - Step 3: Change education to be 3 instead of 2 categories
- What was done: Since following are the frequencies:

        1    583
        2     40
        3     73
        4      4  
    and there aren't enough 4s, combine 3 and 4, and map everything to 0, 1, 2 instead of 1, 2, 3
- Conclusion: Doesn't seem to make a difference both on accuracies and weights (besides the Education weight, but that's because now Education is standardized)
    Committing, but will be reverted to stay with what was done in the course
    
## Step 4: make age categorical, split into bins
Try to split age into groups of more or less equal size. Splitting into 5 groups yielded a worse result:
- Training Score: 0.771, testing score .729
- Intercept and coefficients sorted:

                          Features     Coefs  Odds_ratio
        0                Intercept -1.669344    0.188371
        9                Age_39_40 -0.228201    0.795965
        14                    Pets -0.225331    0.798252
        12               Education -0.181986    0.833613
        10               Age_41_48  0.012772    1.012854
        11         Body Mass Index  0.158052    1.171227
        5              Month Value  0.176372    1.192881
        13                Children  0.201926    1.223757
        8                Age_37_38  0.322398    1.380434
        7                Age_31_36  0.596360    1.815498
        6   Transportation Expense  0.649365    1.914324
        4                 Reason_4  0.675607    1.965226
        2                 Reason_2  0.880699    2.412585
        1                 Reason_1  2.632106   13.903019
        3                 Reason_3  2.900696   18.186802
- Mainly no difference, where there are slight differences:
    - Education becomes less important (perhaps because age and education have a correlation)
    - BMI becomes less important (perhaps because age and BMI have high correlation)
    - Children becomes less important (perhaps because age and number of children have a higher correlation)
### Conclusions:
- Try with smaller and larger number of bins

## Step 5: playing with different age categories (more / less than 5) 
- Made no difference or slightly worse difference
### Conclusions:
- Try without age altogether

## Step 6: no age altogether 
- Made no difference or slightly worse difference
### Conclusions:
- Leave age as was in the lecture