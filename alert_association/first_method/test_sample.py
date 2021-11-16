import pandas as pd

# Intra night association testing

# intra_night_separation_association testing

intra_sep_left_expected = pd.DataFrame(
    {
        "ra": [
            100.000,
            100.000,
            100.003,
            100.003,
            100.007,
            100.007,
            14.000,
            14.000,
            14.003,
            14.003,
            14.007,
            14.007,
        ],
        "dec": [
            8.000,
            8.000,
            8.002,
            8.002,
            8.005,
            8.005,
            16.000,
            16.000,
            15.998,
            15.998,
            15.992,
            15.992,
        ],
        "candid": [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6],
        "traj": [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2],
    }
)

intra_sep_right_expected = pd.DataFrame(
    {
        "ra": [
            100.003,
            100.007,
            100.000,
            100.007,
            100.000,
            100.003,
            14.003,
            14.007,
            14.000,
            14.007,
            14.000,
            14.003,
        ],
        "dec": [
            8.002,
            8.005,
            8.000,
            8.005,
            8.000,
            8.002,
            15.998,
            15.992,
            16.000,
            15.992,
            16.000,
            15.998,
        ],
        "candid": [2, 3, 1, 3, 1, 2, 5, 6, 4, 6, 4, 5],
        "traj": [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2],
    }
)

# compute_diff_mag testing

same_fid_left_expected1 = pd.DataFrame(
    {
        "ra": [
            100.000,
            100.000,
            100.003,
            100.003,
            100.007,
            100.007,
            100.001,
            100.001,
            100.003,
            100.003,
            100.008,
            100.008,
        ],
        "dec": [
            12.000,
            12.000,
            11.998,
            11.998,
            11.994,
            11.994,
            11.994,
            11.994,
            11.998,
            11.998,
            12.002,
            12.002,
        ],
        "jd": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        "dcmag": [
            17.00,
            17.00,
            17.05,
            17.05,
            17.09,
            17.09,
            15.00,
            15.00,
            15.07,
            15.07,
            15.10,
            15.10,
        ],
        "fid": [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2],
        "candid": [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6],
        "traj": [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2],
    }
)


same_fid_right_expected1 = pd.DataFrame(
    {
        "ra": [
            100.003,
            100.007,
            100.000,
            100.007,
            100.000,
            100.003,
            100.003,
            100.008,
            100.001,
            100.008,
            100.001,
            100.003,
        ],
        "dec": [
            11.998,
            11.994,
            12.000,
            11.994,
            12.000,
            11.998,
            11.998,
            12.002,
            11.994,
            12.002,
            11.994,
            11.998,
        ],
        "jd": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        "dcmag": [
            17.05,
            17.09,
            17.00,
            17.09,
            17.00,
            17.05,
            15.07,
            15.10,
            15.00,
            15.10,
            15.00,
            15.07,
        ],
        "fid": [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2],
        "candid": [2, 3, 1, 3, 1, 2, 5, 6, 4, 6, 4, 5],
        "traj": [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2],
    }
)


same_fid_left_expected2 = pd.DataFrame(
    {
        "ra": [100.0, 99.0, 99.8, 100.2, 100.7, 100.5],
        "dec": [12.0, 11.8, 11.2, 12.3, 11.7, 11.5],
        "jd": [1.05, 1.08, 1.09, 2.50, 2.60, 2.70],
        "dcmag": [15.00, 17.00, 16.00, 16.04, 17.03, 15.06],
        "fid": [1, 1, 1, 1, 1, 1],
        "candid": [1, 2, 3, 4, 5, 6],
        "traj": [1, 2, 3, 3, 2, 1],
    }
)


same_fid_right_expected2 = pd.DataFrame(
    {
        "ra": [100.5, 100.7, 100.2, 99.8, 99.0, 100.0],
        "dec": [11.5, 11.7, 12.3, 11.2, 11.8, 12.0],
        "jd": [2.70, 2.60, 2.50, 1.09, 1.08, 1.05],
        "dcmag": [15.06, 17.03, 16.04, 16.00, 17.00, 15.00],
        "fid": [1, 1, 1, 1, 1, 1],
        "candid": [6, 5, 4, 3, 2, 1],
        "traj": [1, 2, 3, 3, 2, 1],
    }
)


# intra_night_association testing

intra_night_test_traj = pd.DataFrame(
    {
        "ra": [
            106.305259,
            106.141905,
            169.860467,
            106.303285,
            106.141138,
            169.856885,
            106.140906,
            106.302386,
            106.140840,
            106.302364,
            169.833666,
            169.829712,
            169.829656,
        ],
        "dec": [
            18.176682,
            15.241181,
            15.206360,
            18.177874,
            15.239999,
            15.210309,
            15.239506,
            18.178404,
            15.239482,
            18.178424,
            15.236048,
            15.240389,
            15.240490,
        ],
        "dcmag": [
            0.066603,
            0.018517,
            0.038709,
            0.089385,
            0.020256,
            0.044030,
            0.021575,
            0.042095,
            0.023033,
            0.046602,
            0.032183,
            0.026171,
            0.025890,
        ],
        "ssnamenr": [
            3866,
            3051,
            19743,
            3866,
            3051,
            19743,
            3051,
            3866,
            3051,
            3866,
            19743,
            19743,
            19743,
        ],
        "fid": [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2],
        "candid": [
            1520166712915015010,
            1520166711415015012,
            1520220641415015001,
            1520227401615015011,
            1520227400315015018,
            1520239140315015026,
            1520254695615015016,
            1520255162915015021,
            1520255630315015010,
            1520255631615015014,
            1520359440315015016,
            1520379906015015006,
            1520380381415015018,
        ],
        "jd": [
            2459274.666713,
            2459274.666713,
            2459274.7206481,
            2459274.7274074,
            2459274.7274074,
            2459274.7391435,
            2459274.7546991,
            2459274.755162,
            2459274.7556366,
            2459274.7556366,
            2459274.8594444,
            2459274.8799074,
            2459274.8803819,
        ],
    }
)

intra_night_left = pd.DataFrame(
    {
        "ra": [
            106.140906,
            106.302386,
            169.829712,
            106.141905,
            106.305259,
            169.860467,
            106.141138,
            106.303285,
            169.856885,
            169.833666,
        ],
        "dec": [
            15.239506,
            18.178404,
            15.240389,
            15.241181,
            18.176682,
            15.20636,
            15.239999,
            18.177874,
            15.210309,
            15.236048,
        ],
        "dcmag": [
            0.021575,
            0.042095,
            0.026171,
            0.018517,
            0.066603,
            0.038709,
            0.020256,
            0.089385,
            0.04403,
            0.032183,
        ],
        "ssnamenr": [3051, 3866, 19743, 3051, 3866, 19743, 3051, 3866, 19743, 19743],
        "fid": [2, 2, 2, 1, 1, 1, 1, 1, 1, 2],
        "candid": [
            1520254695615015016,
            1520255162915015021,
            1520379906015015006,
            1520166711415015012,
            1520166712915015010,
            1520220641415015001,
            1520227400315015018,
            1520227401615015011,
            1520239140315015026,
            1520359440315015016,
        ],
        "jd": [
            2459274.754699,
            2459274.755162,
            2459274.879907,
            2459274.666713,
            2459274.666713,
            2459274.720648,
            2459274.727407,
            2459274.727407,
            2459274.739144,
            2459274.859444,
        ],
    }
)

intra_night_right = pd.DataFrame(
    {
        "ra": [
            106.14084,
            106.302364,
            169.829656,
            106.141138,
            106.303285,
            169.856885,
            106.140906,
            106.302386,
            169.833666,
            169.829712,
        ],
        "dec": [
            15.239482,
            18.178424,
            15.24049,
            15.239999,
            18.177874,
            15.210309,
            15.239506,
            18.178404,
            15.236048,
            15.240389,
        ],
        "dcmag": [
            0.023033,
            0.046602,
            0.02589,
            0.020256,
            0.089385,
            0.04403,
            0.021575,
            0.042095,
            0.032183,
            0.026171,
        ],
        "ssnamenr": [3051, 3866, 19743, 3051, 3866, 19743, 3051, 3866, 19743, 19743],
        "fid": [2, 2, 2, 1, 1, 1, 2, 2, 2, 2],
        "candid": [
            1520255630315015010,
            1520255631615015014,
            1520380381415015018,
            1520227400315015018,
            1520227401615015011,
            1520239140315015026,
            1520254695615015016,
            1520255162915015021,
            1520359440315015016,
            1520379906015015006,
        ],
        "jd": [
            2459274.755637,
            2459274.755637,
            2459274.880382,
            2459274.727407,
            2459274.727407,
            2459274.739144,
            2459274.754699,
            2459274.755162,
            2459274.859444,
            2459274.879907,
        ],
    }
)
