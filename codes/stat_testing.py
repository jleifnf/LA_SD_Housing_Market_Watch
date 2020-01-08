import numpy as np
from scipy import stats


def chi2_contingency(d1_1, d1_2, d2_1, d2_2):
    f_obs = np.array([[d1_1.shape[0], d1_2.shape[0]],
                      [d2_1.shape[0], d2_2.shape[0]]])
    chi2_stats = stats.chi2_contingency(f_obs)[0:3]
    ddof = (f_obs.shape[0] - 1) * (f_obs.shape[1] - 1)
    print(f'X^2({ddof})={chi2_stats[0]}: p={chi2_stats[1]}')


def welch_test(d1,d2, columns=None):
    if columns:
        for col in columns:
            _,p = stats.ttest_ind(d1[col], d2[col], equal_var=False)
            print(f'{col}: p={p}; {"Null-hypothesis rejected." if p < 0.05 else "Cannot reject null-hypothesis." }')
    else:
        _,p = stats.ttest_ind(d1, d2, equal_var=False)
        print(f'p={p}; {"Null-hypothesis rejected." if p < 0.05 else "Cannot reject null-hypothesis." }')
