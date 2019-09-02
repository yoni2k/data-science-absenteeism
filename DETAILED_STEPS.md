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
- Score: 0.78 - .775 (up from previous 0.77 - so removing was helpful), test score: 0.75
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

## Step 7: split day of week to be categorical variable
- Combine Saturday, Sunday to be like Monday
- Result: worse results, to be reverted

## Step 8: group months by season
- Group months by season and make categorical, remove summer (least frequent absenteeisms)
- Result: score slightly higher or same: .784, but test score probably lower: .694
### Conclusions:
- Try categorical but without grouping into season

## Step 9: make month categorical
- And remove lowest frequency - 6

        Frequences of months:
        3     87
        2     72
        10    71
        11    63
        5     58
        7     55
        8     54
        9     53
        4     53
        1     50
        12    49
        6     35
- Score: .782 (same or better), testing .729 (same or better)
- Doesn't change much of the other other weights
### Conclusions:
- Slightly better, but not enough to take it and be different than what was done in the lecture

## Step 10: Remove reasons
- Reasons don't make sense to be in the model (unless we split absences into days), since we only know them after the fact.
- Try to remove reasons.  Expectation: model would have less explanatory power, but other features' influence would be much clearer
- Results: Score of training 0.646, and of testing .6 - less as we expected
- Intercept and coefficients:

                         Features     Coefs  Odds_ratio
        0               Intercept -0.220548    0.802079
        7                    Pets -0.211354    0.809488
        3                     Age -0.072412    0.930148
        1             Month Value  0.126572    1.134931
        5               Education  0.130027    1.138859
        4         Body Mass Index  0.150391    1.162289
        6                Children  0.282478    1.326412
        2  Transportation Expense  0.520165    1.682306
### Conclusions:
- Try to improve by reading what was previously deleted, and adding categorization as I did for some features

## Step 11: Re-add all features
- Re-add all features to double check that ones removed were not because they didn't help when reasons were in
- score of training: 0.659, score of testing: 0.607 - both slightly better
### Conclusions:
- **Distance to Work** clearly doesn't help, remove, leave the rest for now (will remove later after finished adding everything properly)

## Step 12: Remove Distance to Work again
- Since was with a very close to 1 weight: .967
- score of training: 0.664, score of testing: 0.607 - slightly better
- Intercept and coefficients sorted:
                          Features     Coefs  Odds_ratio
        0                Intercept -0.233036    0.792125
        9                     Pets -0.229966    0.794561
        2          Day of the Week -0.196784    0.821368
        4                      Age -0.069003    0.933324
        5  Daily Work Load Average  0.142422    1.153063
        6          Body Mass Index  0.155175    1.167862
        1              Month Value  0.170197    1.185538
        7                Education  0.190926    1.210370
        8                 Children  0.311329    1.365238
        3   Transportation Expense  0.534922    1.707315
### Conclusions:
- Read age, education, day of week, and month as did previously, but this time without reasons

## Step 13: Redo education, then age categories
- Splitting Education into more groups (3 instead of 2) makes the results worse
- Splitting ages into age groups makes it slightly slightly better: score of training: 0.668, score of testing: 0.636
- Intercept and coefficients sorted:

                           Features     Coefs  Odds_ratio
        6                 Age_47_58 -0.487560    0.614123
        0                 Intercept -0.260360    0.770774
        2           Day of the Week -0.195134    0.822725
        11                     Pets -0.170691    0.843082
        5                 Age_40_46  0.116341    1.123379
        7   Daily Work Load Average  0.137455    1.147350
        4                 Age_34_39  0.143244    1.154011
        1               Month Value  0.164338    1.178612
        8           Body Mass Index  0.167356    1.182175
        9                 Education  0.216286    1.241457
        10                 Children  0.319037    1.375802
        3    Transportation Expense  0.518577    1.679635
### Conclusions:
- Out of 3 groups: young people, middle age and slightly older, middle age miss the most (kids?), young in the middle, and older - least
- Probably better to stay with this conclusion, although it helps only slightly (although the conclusion is sound).  Need to decide if worth it to split from the course for it

## Step 14: Split day of week into categories
- score of training: 0.666, score of testing: 0.657 (same or better)
- Intercept and coefficients sorted:

                       Features     Coefs  Odds_ratio
    0                 Intercept -0.694880    0.499134
    14                     Pets -0.166691    0.846461
    5                   Day_Fri -0.125483    0.882071
    4                   Day_Wed -0.034806    0.965792
    3                   Day_Tue -0.033948    0.966622
    13                 Children  0.021066    1.021289
    11          Body Mass Index  0.057955    1.059667
    10  Daily Work Load Average  0.122796    1.130653
    1               Month Value  0.154693    1.167300
    12                Education  0.206839    1.229784
    9                 Age_47_58  0.216159    1.241300
    8                 Age_40_46  0.265714    1.304362
    2                   Day_Mon  0.285967    1.331049
    6    Transportation Expense  0.665392    1.945253
    7                 Age_34_39  1.189535    3.285552
### Conclusions:
- There is less of a chance to be absent on Friday, and more on Sunday
- Drop Tuesday and Wednesday

## Step 15: Leave only Friday and Monday as days
- Because Tuesday-Thursday, there is no special behavior - remove it.  Leave only Friday and Monday, where it's clearly seen that Friday there is less of a chance, and Monday more of a chance
- score of training: 0.662, score of testing: 0.664 - same or better
- Intercept and coefficients sorted:
        
                           Features     Coefs  Odds_ratio
        0                 Intercept -0.719551    0.486971
        12                     Pets -0.166393    0.846714
        3                   Day_Fri -0.103032    0.902098
        11                 Children  0.021654    1.021890
        9           Body Mass Index  0.057774    1.059476
        8   Daily Work Load Average  0.122444    1.130256
        1               Month Value  0.154902    1.167544
        10                Education  0.208551    1.231892
        7                 Age_47_58  0.216748    1.242031
        6                 Age_40_46  0.268306    1.307747
        2                   Day_Mon  0.308954    1.361999
        4    Transportation Expense  0.665532    1.945524
        5                 Age_34_39  1.188558    3.282345
### Conclusions:
- Leave for now Fridays and Sundays, decide later if worth to deviate from course

## Step 16: Split into specific months
- score of training: 0.689, score of testing: 0.657 - similar
- Intercept and coefficients sorted:

        1                   Month_1 -1.017627    0.361452
        2                   Month_2 -0.799833    0.449404
        5                   Month_5 -0.568547    0.566348
        8                   Month_9 -0.491489    0.611715
        9                  Month_10 -0.471914    0.623807
        0                 Intercept -0.415403    0.660074
        3                   Month_3 -0.244776    0.782880
        10                 Month_11 -0.220430    0.802174
        22                     Pets -0.177009    0.837772
        13                  Day_Fri -0.158069    0.853791
        11                 Month_12 -0.071723    0.930788
        21                 Children  0.056414    1.058036
        17                Age_47_58  0.059714    1.061533
        19          Body Mass Index  0.096715    1.101547
        4                   Month_4  0.114295    1.121082
        16                Age_40_46  0.232944    1.262310
        18  Daily Work Load Average  0.243870    1.276179
        20                Education  0.249014    1.282760
        12                  Day_Mon  0.254595    1.289939
        7                   Month_8  0.466115    1.593790
        14   Transportation Expense  0.621735    1.862156
        6                   Month_7  0.909284    2.482546
        15                Age_34_39  1.079998    2.944672        
### Conclusions:
- Clearly see that in some months there is a lot more absenteeism, like 7,8, and in some less.
- However, month 12 seems not to add a lot of info compared to month 6 reference category, to remove

## Step 17: Remove also month 12
- score of training: 0.684, score of testing: 0.657 - similar
- Intercept and coefficients sorted:

                           Features     Coefs  Odds_ratio
        1                   Month_1 -0.997929    0.368642
        2                   Month_2 -0.777001    0.459783
        5                   Month_5 -0.546803    0.578797
        8                   Month_9 -0.469519    0.625303
        9                  Month_10 -0.448517    0.638574
        0                 Intercept -0.441546    0.643042
        3                   Month_3 -0.221460    0.801348
        10                 Month_11 -0.198123    0.820269
        21                     Pets -0.179053    0.836062
        12                  Day_Fri -0.159777    0.852334
        20                 Children  0.055890    1.057481
        16                Age_47_58  0.061026    1.062927
        18          Body Mass Index  0.097543    1.102459
        4                   Month_4  0.137001    1.146829
        15                Age_40_46  0.233753    1.263333
        17  Daily Work Load Average  0.246496    1.279534
        19                Education  0.250723    1.284954
        11                  Day_Mon  0.257278    1.293405
        7                   Month_8  0.490307    1.632817
        13   Transportation Expense  0.623077    1.864657
        6                   Month_7  0.933111    2.542406
        14                Age_34_39  1.080407    2.945879       
### Conclusions:
- Especially clear that in July - August there is a lot of absenteeism
- Consider removing Children since very low weight - strange, but perhaps the age explains better than number of children whether someone will be missing (maybe need a category of number of small children)?

## Step 18: Remove number of children
- Remove children since very low weight - strange, but perhaps the age explains better than number of children whether someone will be missing (maybe need a category of number of small children)?
- score of training: 0.689, score of testing: 0.65 - similar
- Intercept and coefficients sorted:

                           Features     Coefs  Odds_ratio
        1                   Month_1 -1.004155    0.366354
        2                   Month_2 -0.784740    0.456238
        5                   Month_5 -0.538904    0.583387
        0                 Intercept -0.470517    0.624679
        8                   Month_9 -0.467160    0.626780
        9                  Month_10 -0.442828    0.642218
        3                   Month_3 -0.207727    0.812429
        10                 Month_11 -0.193699    0.823906
        20                     Pets -0.181566    0.833963
        12                  Day_Fri -0.144845    0.865156
        18          Body Mass Index  0.078925    1.082123
        16                Age_47_58  0.122772    1.130626
        4                   Month_4  0.137024    1.146856
        19                Education  0.228439    1.256637
        15                Age_40_46  0.240078    1.271348
        17  Daily Work Load Average  0.245621    1.278415
        11                  Day_Mon  0.258970    1.295595
        7                   Month_8  0.487519    1.628271
        13   Transportation Expense  0.646782    1.909386
        6                   Month_7  0.922204    2.514826
        14                Age_34_39  1.146026    3.145666   
### Conclusions:
- Seems that removing children doesn't do harm.  However, I think there are too many months that add a lot of noise.  It seems that 7-8 months are the unusual ones.
- Return children for now, and just put if it's July-August

## Step 19: For months, leave only July August
- July-August indeed has a very high predictor
- score of training: 0.675, score of testing: 0.679 - similar
- Intercept and coefficients sorted:

                           Features     Coefs  Odds_ratio
        0                 Intercept -0.808164    0.445676
        12                     Pets -0.167743    0.845571
        3                   Day_Fri -0.092570    0.911585
        7                 Age_47_58  0.069671    1.072155
        11                 Children  0.074388    1.077225
        9           Body Mass Index  0.089456    1.093579
        10                Education  0.205064    1.227604
        8   Daily Work Load Average  0.220771    1.247038
        6                 Age_40_46  0.233066    1.262465
        2                   Day_Mon  0.258053    1.294407
        4    Transportation Expense  0.627864    1.873604
        5                 Age_34_39  1.065440    2.902116
        1                  July_Aug  1.070878    2.917940
### Conclusions:
- Seems that leaving only July, August has much more explanatory power
- Remove or Age 47-58, or children, and see what's better - both low, but can affect each other

## Step 20: Age - find most interesting age group
- Age groups don't give consistent results, not in high absenteeism, not in low
- See details in files/ages.xlsx
### Conclusions:
- Committing code to search for different groups, to be reverted

## Step 21: Age - remove age 47-58
- Same or slightly better result, leave like this: score of training: 0.677, score of testing: 0.679
- Intercept and coefficients sorted:

                           Features     Coefs  Odds_ratio
        0                 Intercept -0.784529    0.456335
        11                     Pets -0.169205    0.844336
        3                   Day_Fri -0.092458    0.911688
        10                 Children  0.082304    1.085785
        8           Body Mass Index  0.103971    1.109568
        9                 Education  0.205684    1.228364
        6                 Age_40_46  0.209339    1.232863
        7   Daily Work Load Average  0.222244    1.248876
        2                   Day_Mon  0.258389    1.294843
        4    Transportation Expense  0.623646    1.865718
        5                 Age_34_39  1.036091    2.818180
        1                  July_Aug  1.075593    2.931730
   
### Conclusions:
- Try without children 

## Step 22: Remove children
- score of training: 0.682, score of testing: 0.693 - slightly better
- Intercept and coefficients sorted:

                           Features     Coefs  Odds_ratio
        0                 Intercept -0.793816    0.452116
        10                     Pets -0.175972    0.838641
        3                   Day_Fri -0.068323    0.933958
        8           Body Mass Index  0.094045    1.098609
        9                 Education  0.171469    1.187047
        6                 Age_40_46  0.184562    1.202691
        7   Daily Work Load Average  0.220908    1.247209
        2                   Day_Mon  0.262682    1.300412
        4    Transportation Expense  0.659214    1.933271
        1                  July_Aug  1.064144    2.898356
        5                 Age_34_39  1.102984    3.013145   
### Conclusions:
- Stay without children for now - slightly better, remove Friday

## Step 22: Remove Friday
- score of training: 0.682, score of testing: 0.686 - same, slightly worse, but more explanatory power
- Intercept and coefficients sorted:

        0                Intercept -0.807425    0.446005
        9                     Pets -0.174527    0.839854
        7          Body Mass Index  0.097473    1.102381
        8                Education  0.170974    1.186459
        5                Age_40_46  0.180661    1.198008
        6  Daily Work Load Average  0.222087    1.248680
        2                  Day_Mon  0.277416    1.319716
        3   Transportation Expense  0.657582    1.930119
        1                 July_Aug  1.065216    2.901465
        4                Age_34_39  1.097422    2.996430
### Conclusions:
- Not because of numbers, but a feeling - remove Education, since has high correlation to age, and gut feeling doesn't have to do with missing work

## Step 23: Remove Education
- score of training: 0.682, score of testing: 0.686 - same - Education doesn't help
- Intercept and coefficients sorted:

                          Features     Coefs  Odds_ratio
        0                Intercept -0.767569    0.464140
        8                     Pets -0.183386    0.832447
        7          Body Mass Index  0.073662    1.076443
        5                Age_40_46  0.163434    1.177547
        6  Daily Work Load Average  0.216384    1.241579
        2                  Day_Mon  0.281451    1.325051
        3   Transportation Expense  0.654651    1.924470
        1                 July_Aug  1.059767    2.885699
        4                Age_34_39  1.073777    2.926411
### Conclusions:
- Not because of numbers, but a feeling - remove BMI - doesn't seem to help a lot

## Step 24: Remove BMI
- score of training: 0.679, score of testing: 0.7 - better - BMI doesn't help
- Intercept and coefficients sorted:

                          Features     Coefs  Odds_ratio
        0                Intercept -0.778874    0.458923
        7                     Pets -0.178859    0.836224
        5                Age_40_46  0.185228    1.203493
        6  Daily Work Load Average  0.210036    1.233723
        2                  Day_Mon  0.292414    1.339657
        3   Transportation Expense  0.643484    1.903100
        1                 July_Aug  1.065122    2.901194
        4                Age_34_39  1.077213    2.936484
### Conclusions:
- Try to re-add children, see if it helps

## Step 25: Readding children
- score of training: 0.67, score of testing: 0.693 - slightly worse
- Children don't help
- Intercept and coefficients sorted:

                          Features     Coefs  Odds_ratio
        0                Intercept -0.771112    0.462499
        8                     Pets -0.175529    0.839013
        7                 Children  0.051258    1.052595
        5                Age_40_46  0.198394    1.219443
        6  Daily Work Load Average  0.210018    1.233701
        2                  Day_Mon  0.293855    1.341590
        3   Transportation Expense  0.620203    1.859305
        4                Age_34_39  1.032032    2.806763
        1                 July_Aug  1.072150    2.921654
### Conclusions:
- Revert adding children

## Step 26: Remove children again
- score of training: 0.679, score of testing: 0.7 - best so far
- Intercept and coefficients sorted:

                          Features     Coefs  Odds_ratio
        0                Intercept -0.778874    0.458923
        7                     Pets -0.178859    0.836224
        5                Age_40_46  0.185228    1.203493
        6  Daily Work Load Average  0.210036    1.233723
        2                  Day_Mon  0.292414    1.339657
        3   Transportation Expense  0.643484    1.903100
        1                 July_Aug  1.065122    2.901194
        4                Age_34_39  1.077213    2.936484
### Conclusions:
- Bottom line biggest predictors of absenteesm is:
    - Certain age group (we could probably search for even better groups, although initial search didn't yield any conclusive results)
    - July - August is a big predictor
    - Monday is a big predictor
    - More of transportation expenses - more chance to miss
    - Working more has some explanation for missing work
    - Finally if there are pets at home, there is less chance to miss work (interesting!)
