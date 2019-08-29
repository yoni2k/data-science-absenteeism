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
         