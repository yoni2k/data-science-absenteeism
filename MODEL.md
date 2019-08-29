# Steps of Changes to the model:
## Step 1: Give an option not to standardize dummy variables for better interpretability
Especially to understand how Reasons effect the model exactly
### Values before removing standardizing dummies:
- Score: 0.78
- Intercept and coefficients sorted:
---
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