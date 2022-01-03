import pandas as pd
import numpy as np

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


# Night to night association testing

# Cone search association testing

# Association that match the angle criterion
cone_search_two_last_observation_sample = pd.DataFrame(
    {
        "ra": [1, 2, 4, 5, 5, 6, 1, 2],
        "dec": [8, 7, 1, 2, 4, 8, 1, 1],
        "jd": [1, 2, 1, 2, 1, 2, 1, 2],
        "candid": [10, 11, 12, 13, 14, 15, 16, 17],
        "trajectory_id": [20, 20, 21, 21, 22, 22, 23, 23],
    }
)

traj_assoc_sample = pd.DataFrame(
    {
        "ra": [2, 5, 6, 2],
        "dec": [7, 2, 8, 1],
        "jd": [2, 2, 2, 2],
        "candid": [11, 13, 15, 17],
        "trajectory_id": [20, 21, 22, 23],
    }
)

new_obs_assoc_sample = pd.DataFrame(
    {
        "ra": [3, 6, 7, 3],
        "dec": [6, 3, 9, 1],
        "jd": [3, 3, 3, 3],
        "candid": [18, 19, 20, 21],
        "trajectory_id": [30, 31, 32, 33],
    }
)

left_cone_search_expected = pd.DataFrame(
    {
        "ra": [2, 5, 6, 2],
        "dec": [7, 2, 8, 1],
        "jd": [2, 2, 2, 2],
        "candid": [11, 13, 15, 17],
        "trajectory_id": [20, 21, 22, 23],
    }
)

right_cone_search_expected = pd.DataFrame(
    {
        "ra": [3, 6, 7, 3],
        "dec": [6, 3, 9, 1],
        "jd": [3, 3, 3, 3],
        "candid": [18, 19, 20, 21],
        "tmp_traj": [30, 31, 32, 33],
        "trajectory_id": [20, 21, 22, 23],
    }
)

# Association that not match the angle criterion
false_cone_search_two_last_observation_sample = pd.DataFrame(
    {
        "ra": [2, 3, 8, 9, 7, 8],
        "dec": [1, 2, 2, 3, 5, 6],
        "jd": [1, 2, 1, 2, 1, 2],
        "candid": [10, 11, 12, 13, 14, 15],
        "trajectory_id": [20, 20, 21, 21, 22, 22],
    }
)

false_traj_assoc_sample = pd.DataFrame(
    {
        "ra": [3, 9, 8],
        "dec": [2, 3, 6],
        "jd": [2, 2, 2],
        "candid": [11, 13, 15],
        "trajectory_id": [20, 21, 22],
    }
)

false_new_obs_assoc_sample = pd.DataFrame(
    {
        "ra": [4, 8, 7],
        "dec": [1, 5, 7],
        "jd": [3, 3, 3],
        "candid": [16, 17, 18],
        "trajectory_id": [30, 31, 32],
    }
)

# Night to night trajectory association testing

night_to_night_two_last_sample = pd.DataFrame(
    {
        "ra": [1, 2, 5, 6, 10, 11, 1, 2, 7, 7, 1, 8],
        "dec": [1, 2, 1, 1, 1, 1, 6, 7, 7, 8, 11, 6],
        "dcmag": [13, 13.05, 15, 15.08, 17, 17.03, 16, 16.04, 17, 17.1, 14, 18],
        "fid": [1, 2, 1, 1, 2, 2, 1, 2, 2, 2, 1, 1],
        "jd": [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2],
        "candid": [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21],
        "trajectory_id": [0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5],
    }
)

night_to_night_new_observation = pd.DataFrame(
    {
        "ra": [3, 7, 10.5, 2, 3, 4, 11, 8],
        "dec": [3, 2, 2, 8, 7, 9, 9, 9],
        "dcmag": [13.1, 15.13, 17.06, 16.07, 16.05, 15, 18, 18.5],
        "fid": [2, 1, 1, 1, 2, 1, 2, 2],
        "jd": [3, 3, 3, 3, 3, 3, 3, 3],
        "candid": [22, 23, 24, 25, 26, 27, 28, 29],
    }
)

night_to_night_traj_assoc_left_expected = pd.DataFrame(
    {
        "trajectory_id": [0, 1, 3, 3],
        "ra": [2, 6, 2, 2],
        "dec": [2, 1, 7, 7],
        "dcmag": [13.05, 15.08, 16.04, 16.04],
        "fid": [2, 1, 2, 2],
        "jd": [2, 2, 2, 2],
        "candid": [11, 13, 17, 17],
    }
)

night_to_night_traj_assoc_right_expected = pd.DataFrame(
    {
        "ra": [3.0, 7, 3, 2],
        "dec": [3, 2, 7, 8],
        "dcmag": [13.10, 15.13, 16.05, 16.07],
        "fid": [2, 1, 2, 1],
        "jd": [3, 3, 3, 3],
        "candid": [22, 23, 26, 25],
        "trajectory_id": [0, 1, 3, 3],
    }
)


# trajectory associations testing

trajectory_df_sample = pd.DataFrame(
    {
        "ra": [1, 2, 3, 1, 2, 2, 6, 7, 8, 6, 7, 8, 9, 10, 10],
        "dec": [1, 2, 3, 12, 11, 10, 12, 12, 12, 6, 5, 6, 1, 2, 3],
        "dcmag": [
            12.02,
            12.05,
            12.3,
            15,
            15.1,
            15.23,
            13,
            12.6,
            12.75,
            17.02,
            17.15,
            17.27,
            16,
            16.4,
            16.7,
        ],
        "fid": [1, 1, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 1],
        "nid": [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3],
        "jd": [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3],
        "candid": [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24],
        "trajectory_id": [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5],
    }
)

traj_next_night_sample = pd.DataFrame(
    {
        "ra": [4, 5, 1, 1, 8, 7, 13, 13],
        "dec": [4, 5, 9, 8, 7, 8, 1, 2],
        "dcmag": [12.4, 12.52, 15.94, 15.47, 17.31, 17.43, 16.21, 16.28],
        "fid": [1, 1, 2, 1, 1, 1, 2, 2],
        "nid": [4, 4, 4, 4, 4, 4, 4, 4],
        "jd": [4.1, 4.2, 4.1, 4.2, 4.1, 4.2, 4.1, 4.2],
        "candid": [25, 26, 27, 28, 29, 30, 31, 32],
        "trajectory_id": [10, 10, 11, 11, 12, 12, 13, 13],
    }
)

new_observations_sample = pd.DataFrame(
    {
        "ra": [5, 5, 10, 9, 13],
        "dec": [1, 10, 4, 10, 11],
        "dcmag": [13.42, 17.5, 16.82, 15.86, 16.49],
        "fid": [2, 2, 1, 2, 1],
        "nid": [4, 4, 4, 4, 4],
        "jd": [4.1, 4.2, 4.2, 4.2, 4.3],
        "candid": [33, 34, 35, 36, 37],
    }
)

trajectory_df_expected = pd.DataFrame(
    {
        "ra": [1, 2, 3, 1, 2, 2, 6, 7, 8, 6, 7, 8, 9, 10, 10, 4, 5, 8, 7, 10],
        "dec": [1, 2, 3, 12, 11, 10, 12, 12, 12, 6, 5, 6, 1, 2, 3, 4, 5, 7, 8, 4],
        "dcmag": [
            12.02,
            12.05,
            12.30,
            15.00,
            15.10,
            15.23,
            13.00,
            12.60,
            12.75,
            17.02,
            17.15,
            17.27,
            16.00,
            16.40,
            16.70,
            12.40,
            12.52,
            17.31,
            17.43,
            16.82,
        ],
        "fid": [1, 1, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 1, 1, 1, 1, 1, 1],
        "nid": [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 4, 4, 4, 4, 4],
        "jd": [
            1.0,
            2.0,
            3.0,
            1.0,
            2.0,
            3.0,
            1.0,
            2.0,
            3.0,
            1.0,
            2.0,
            3.0,
            1.0,
            2.0,
            3.0,
            4.1,
            4.2,
            4.1,
            4.2,
            4.2,
        ],
        "candid": [
            10,
            11,
            12,
            13,
            14,
            15,
            16,
            17,
            18,
            19,
            20,
            21,
            22,
            23,
            24,
            25,
            26,
            29,
            30,
            35,
        ],
        "trajectory_id": [
            1.0,
            1.0,
            1.0,
            2.0,
            2.0,
            2.0,
            3.0,
            3.0,
            3.0,
            4.0,
            4.0,
            4.0,
            5.0,
            5.0,
            5.0,
            1.0,
            1.0,
            4.0,
            4.0,
            5.0,
        ],
    }
)

traj_next_night_expected = pd.DataFrame(
    {
        "ra": [1, 1, 13, 13],
        "dec": [9, 8, 1, 2],
        "dcmag": [15.94, 15.47, 16.21, 16.28],
        "fid": [2, 1, 2, 2],
        "nid": [4, 4, 4, 4],
        "jd": [4.1, 4.2, 4.1, 4.2],
        "candid": [27, 28, 31, 32],
        "trajectory_id": [11, 11, 13, 13],
    }
)

new_observations_expected = pd.DataFrame(
    {
        "ra": [5, 5, 9, 13],
        "dec": [1, 10, 10, 11],
        "dcmag": [13.42, 17.50, 15.86, 16.49],
        "fid": [2, 2, 2, 1],
        "nid": [4, 4, 4, 4],
        "jd": [4.1, 4.2, 4.2, 4.3],
        "candid": [33, 34, 36, 37],
    }
)

trajectory_df_expected2 = pd.DataFrame(
    {
        "ra": [1, 2, 3, 1, 2, 2, 6, 7, 8, 6, 7, 8, 9, 10, 10, 4, 5, 8, 7],
        "dec": [1, 2, 3, 12, 11, 10, 12, 12, 12, 6, 5, 6, 1, 2, 3, 4, 5, 7, 8],
        "dcmag": [
            12.02,
            12.05,
            12.30,
            15.00,
            15.10,
            15.23,
            13.00,
            12.60,
            12.75,
            17.02,
            17.15,
            17.27,
            16.00,
            16.40,
            16.70,
            12.40,
            12.52,
            17.31,
            17.43,
        ],
        "fid": [1, 1, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 1, 1, 1, 1, 1],
        "nid": [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 4, 4, 4, 4],
        "jd": [
            1.0,
            2.0,
            3.0,
            1.0,
            2.0,
            3.0,
            1.0,
            2.0,
            3.0,
            1.0,
            2.0,
            3.0,
            1.0,
            2.0,
            3.0,
            4.1,
            4.2,
            4.1,
            4.2,
        ],
        "candid": [
            10,
            11,
            12,
            13,
            14,
            15,
            16,
            17,
            18,
            19,
            20,
            21,
            22,
            23,
            24,
            25,
            26,
            29,
            30,
        ],
        "trajectory_id": [
            1.0,
            1.0,
            1.0,
            2.0,
            2.0,
            2.0,
            3.0,
            3.0,
            3.0,
            4.0,
            4.0,
            4.0,
            5.0,
            5.0,
            5.0,
            1.0,
            1.0,
            4.0,
            4.0,
        ],
    }
)

trajectory_df_expected_empty = pd.DataFrame(
    {
        "ra": [1, 2, 3, 1, 2, 2, 6, 7, 8, 6, 7, 8, 9, 10, 10, 10],
        "dec": [1, 2, 3, 12, 11, 10, 12, 12, 12, 6, 5, 6, 1, 2, 3, 4],
        "dcmag": [
            12.02,
            12.05,
            12.30,
            15.00,
            15.10,
            15.23,
            13.00,
            12.60,
            12.75,
            17.02,
            17.15,
            17.27,
            16.00,
            16.40,
            16.70,
            16.82,
        ],
        "fid": [1, 1, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 1, 1],
        "nid": [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 4],
        "jd": [
            1.0,
            2.0,
            3.0,
            1.0,
            2.0,
            3.0,
            1.0,
            2.0,
            3.0,
            1.0,
            2.0,
            3.0,
            1.0,
            2.0,
            3.0,
            4.2,
        ],
        "candid": [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 35],
        "trajectory_id": [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 5],
    }
)

expected_trajectory_first_report = {
    "list of updated trajectories": [1.0, 4.0, 5.0],
    "all nid report": [
        {
            "old nid": 3,
            "trajectories_to_tracklets_report": {
                "number of inter night separation based association": 3,
                "number of inter night magnitude filtered association": 1,
                "number of inter night angle filtered association": 0,
                "number of duplicated association": 0,
                "metrics": {},
            },
            "trajectories_to_new_observation_report": {
                "number of inter night separation based association": 1,
                "number of inter night magnitude filtered association": 0,
                "number of inter night angle filtered association": 0,
                "number of duplicated association": 0,
                "metrics": {},
            },
        }
    ],
}


expected_trajectory_second_report = {
    "list of updated trajectories": [5.0],
    "all nid report": [
        {
            "old nid": 3,
            "trajectories_to_tracklets_report": {
                "number of inter night separation based association": 0,
                "number of inter night magnitude filtered association": 0,
                "number of inter night angle filtered association": 0,
                "number of duplicated association": 0,
                "metrics": {},
            },
            "trajectories_to_new_observation_report": {
                "number of inter night separation based association": 1,
                "number of inter night magnitude filtered association": 0,
                "number of inter night angle filtered association": 0,
                "number of duplicated association": 0,
                "metrics": {},
            },
        }
    ],
}

expected_trajectory_third_report = {
    "list of updated trajectories": [],
    "all nid report": [
        {
            "old nid": 3,
            "trajectories_to_tracklets_report": {
                "number of inter night separation based association": 3,
                "number of inter night magnitude filtered association": 1,
                "number of inter night angle filtered association": 0,
                "number of duplicated association": 0,
                "metrics": {},
            },
            "trajectories_to_new_observation_report": {},
        }
    ],
}

# tracklets and observations associations testing

track_and_obs_trajectory_df_sample = pd.DataFrame(
    {
        "ra": [1, 2, 2, 6, 7, 8, 6, 7, 8, 9, 10, 10],
        "dec": [12, 11, 10, 12, 12, 12, 6, 5, 6, 1, 2, 3],
        "dcmag": [
            15,
            15.1,
            15.23,
            13,
            12.6,
            12.75,
            17.02,
            17.15,
            17.27,
            16,
            16.4,
            16.7,
        ],
        "fid": [1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 1],
        "nid": [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3],
        "jd": [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3],
        "candid": [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24],
        "trajectory_id": [2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5],
    }
)

track_and_obs_traj_next_night_sample = pd.DataFrame(
    {
        "ra": [2, 3, 7, 8],
        "dec": [2, 3, 1, 2],
        "dcmag": [15.74, 15.47, 16.21, 16.28],
        "fid": [2, 1, 2, 2],
        "nid": [4, 4, 4, 4],
        "jd": [4.1, 4.2, 4.1, 4.2],
        "candid": [27, 28, 31, 32],
        "trajectory_id": [11, 11, 13, 13],
    }
)

track_and_obs_old_observations_sample = pd.DataFrame(
    {
        "ra": [1, 1, 4, 3, 6, 7, 9],
        "dec": [1, 5, 1, 5, 1, 7, 5],
        "dcmag": [15.52, 16.32, 14.96, 16.28, 16.03, 18.52, 17.68],
        "fid": [2, 1, 2, 2, 2, 1, 1],
        "nid": [2, 1, 3, 3, 3, 3, 3],
        "jd": [2.1, 1.2, 3.1, 3.2, 3.1, 3.2, 3.1],
        "candid": [33, 34, 35, 36, 37, 38, 39],
    }
)

track_and_obs_new_observations_sample = pd.DataFrame(
    {
        "ra": [2, 4, 6, 5, 10],
        "dec": [9, 6, 3, 10, 4],
        "dcmag": [15.52, 16.32, 14.96, 18.52, 17.99],
        "fid": [2, 1, 2, 1, 2],
        "nid": [4, 4, 4, 4, 4],
        "jd": [4.1, 4.2, 4.1, 4.2, 4.1],
        "candid": [40, 41, 42, 43, 44],
    }
)

track_and_obs_trajectory_df_expected = pd.DataFrame(
    {
        "ra": [
            1,
            2,
            2,
            6,
            7,
            8,
            6,
            7,
            8,
            9,
            10,
            10,
            3,
            9,
            4,
            10,
            1,
            2,
            2,
            3,
            7,
            8,
            6,
            1,
        ],
        "dec": [
            12,
            11,
            10,
            12,
            12,
            12,
            6,
            5,
            6,
            1,
            2,
            3,
            5,
            5,
            6,
            4,
            5,
            9,
            2,
            3,
            1,
            2,
            1,
            1,
        ],
        "dcmag": [
            15.00,
            15.10,
            15.23,
            13.00,
            12.60,
            12.75,
            17.02,
            17.15,
            17.27,
            16.00,
            16.40,
            16.70,
            16.28,
            17.68,
            16.32,
            17.99,
            16.32,
            15.52,
            15.74,
            15.47,
            16.21,
            16.28,
            16.03,
            15.52,
        ],
        "fid": [1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 1, 2, 1, 1, 2, 1, 2, 2, 1, 2, 2, 2, 2],
        "nid": [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 3, 3, 4, 4, 1, 4, 4, 4, 4, 4, 3, 2],
        "jd": [
            1.0,
            2.0,
            3.0,
            1.0,
            2.0,
            3.0,
            1.0,
            2.0,
            3.0,
            1.0,
            2.0,
            3.0,
            3.2,
            3.1,
            4.2,
            4.1,
            1.2,
            4.1,
            4.1,
            4.2,
            4.1,
            4.2,
            3.1,
            2.1,
        ],
        "candid": [
            13,
            14,
            15,
            16,
            17,
            18,
            19,
            20,
            21,
            22,
            23,
            24,
            36,
            39,
            41,
            44,
            34,
            40,
            27,
            28,
            31,
            32,
            37,
            33,
        ],
        "trajectory_id": [
            2,
            2,
            2,
            3,
            3,
            3,
            4,
            4,
            4,
            5,
            5,
            5,
            6,
            7,
            6,
            7,
            8,
            8,
            11,
            11,
            13,
            13,
            13,
            11,
        ],
    }
)

track_and_obs_old_observations_expected = pd.DataFrame(
    {
        "ra": [4, 7, 6, 5],
        "dec": [1, 7, 3, 10],
        "dcmag": [14.96, 18.52, 14.96, 18.52],
        "fid": [2, 1, 2, 1],
        "nid": [3, 3, 4, 4],
        "jd": [3.1, 3.2, 4.1, 4.2],
        "candid": [35, 38, 42, 43],
    }
)


track_and_obs_trajectory_df_expected2 = pd.DataFrame(
    {
        "ra": [1, 2, 2, 6, 7, 8, 6, 7, 8, 9, 10, 10, 3, 9, 4, 10, 1, 2],
        "dec": [12, 11, 10, 12, 12, 12, 6, 5, 6, 1, 2, 3, 5, 5, 6, 4, 5, 9],
        "dcmag": [
            15,
            15.1,
            15.23,
            13,
            12.6,
            12.75,
            17.02,
            17.15,
            17.27,
            16,
            16.4,
            16.7,
            16.28,
            17.68,
            16.32,
            17.99,
            16.32,
            15.52,
        ],
        "fid": [1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 1, 2, 1, 1, 2, 1, 2],
        "nid": [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 3, 3, 4, 4, 1, 4],
        "jd": [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 3.2, 3.1, 4.2, 4.1, 1.2, 4.1],
        "candid": [
            13,
            14,
            15,
            16,
            17,
            18,
            19,
            20,
            21,
            22,
            23,
            24,
            36,
            39,
            41,
            44,
            34,
            40,
        ],
        "trajectory_id": [2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 7, 6, 7, 8, 8],
    }
)

track_and_obs_old_observations_expected2 = pd.DataFrame(
    {
        "ra": [1, 4, 6, 7, 6, 5],
        "dec": [1, 1, 1, 7, 3, 10],
        "dcmag": [15.52, 14.96, 16.03, 18.52, 14.96, 18.52],
        "fid": [2, 2, 2, 1, 2, 1],
        "nid": [2, 3, 3, 3, 4, 4],
        "jd": [2.1, 3.1, 3.1, 3.2, 4.1, 4.2],
        "candid": [33, 35, 37, 38, 42, 43],
    }
)

track_and_obs_trajectory_df_expected3 = pd.DataFrame(
    {
        "ra": [3, 9, 4, 10, 1, 2, 2, 3, 7, 8, 6, 1],
        "dec": [5, 5, 6, 4, 5, 9, 2, 3, 1, 2, 1, 1],
        "dcmag": [
            16.28,
            17.68,
            16.32,
            17.99,
            16.32,
            15.52,
            15.74,
            15.47,
            16.21,
            16.28,
            16.03,
            15.52,
        ],
        "fid": [2, 1, 1, 2, 1, 2, 2, 1, 2, 2, 2, 2],
        "nid": [3, 3, 4, 4, 1, 4, 4, 4, 4, 4, 3, 2],
        "jd": [3.2, 3.1, 4.2, 4.1, 1.2, 4.1, 4.1, 4.2, 4.1, 4.2, 3.1, 2.1],
        "candid": [36, 39, 41, 44, 34, 40, 27, 28, 31, 32, 37, 33],
        "trajectory_id": [6, 7, 6, 7, 8, 8, 11, 11, 13, 13, 13, 11],
    }
)

track_and_obs_trajectory_df_expected4 = pd.DataFrame(
    {
        "ra": [1, 2, 2, 6, 7, 8, 6, 7, 8, 9, 10, 10, 2, 3, 7, 8],
        "dec": [12, 11, 10, 12, 12, 12, 6, 5, 6, 1, 2, 3, 2, 3, 1, 2],
        "dcmag": [
            15,
            15.1,
            15.23,
            13,
            12.6,
            12.75,
            17.02,
            17.15,
            17.27,
            16,
            16.4,
            16.7,
            15.74,
            15.47,
            16.21,
            16.28,
        ],
        "fid": [1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 1, 2, 1, 2, 2],
        "nid": [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 4, 4, 4, 4],
        "jd": [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 4.1, 4.2, 4.1, 4.2],
        "candid": [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 27, 28, 31, 32],
        "trajectory_id": [2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 11, 11, 13, 13],
    }
)

track_and_obs_old_observations_expected3 = pd.DataFrame(
    {
        "ra": [2, 4, 6, 5, 10],
        "dec": [9, 6, 3, 10, 4],
        "dcmag": [15.52, 16.32, 14.96, 18.52, 17.99],
        "fid": [2, 1, 2, 1, 2],
        "nid": [4, 4, 4, 4, 4],
        "jd": [4.1, 4.2, 4.1, 4.2, 4.1],
        "candid": [40, 41, 42, 43, 44],
    }
)

track_and_obs_trajectory_df_expected5 = pd.DataFrame(
    {
        "ra": [1, 2, 2, 6, 7, 8, 6, 7, 8, 9, 10, 10, 2, 3, 7, 8, 6, 1],
        "dec": [12, 11, 10, 12, 12, 12, 6, 5, 6, 1, 2, 3, 2, 3, 1, 2, 1, 1],
        "dcmag": [
            15,
            15.1,
            15.23,
            13,
            12.6,
            12.75,
            17.02,
            17.15,
            17.27,
            16,
            16.4,
            16.7,
            15.74,
            15.47,
            16.21,
            16.28,
            16.03,
            15.52,
        ],
        "fid": [1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 1, 2, 1, 2, 2, 2, 2],
        "nid": [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 4, 4, 4, 4, 3, 2],
        "jd": [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 4.1, 4.2, 4.1, 4.2, 3.1, 2.1],
        "candid": [
            13,
            14,
            15,
            16,
            17,
            18,
            19,
            20,
            21,
            22,
            23,
            24,
            27,
            28,
            31,
            32,
            37,
            33,
        ],
        "trajectory_id": [2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 11, 11, 13, 13, 13, 11],
    }
)

track_and_obs_old_observations_expected4 = pd.DataFrame(
    {
        "ra": [1, 4, 3, 7, 9],
        "dec": [5, 1, 5, 7, 5],
        "dcmag": [16.32, 14.96, 16.28, 18.52, 17.68],
        "fid": [1, 2, 2, 1, 1],
        "nid": [1, 3, 3, 3, 3],
        "jd": [1.2, 3.1, 3.2, 3.2, 3.1],
        "candid": [34, 35, 36, 38, 39],
    }
)

expected_traj_obs_report = {
    "list of updated trajectories": [6.0, 7.0, 8.0, 11.0, 13.0],
    "all nid report": [
        {
            "old nid": 3,
            "old observation to tracklets report": {
                "number of inter night separation based association": 1,
                "number of inter night magnitude filtered association": 0,
                "number of inter night angle filtered association": 0,
                "number of duplicated association": 0,
                "metrics": {},
            },
            "old observation to new observation report": {
                "number of inter night separation based association": 2,
                "number of inter night magnitude filtered association": 0,
                "number of duplicated association": 0,
                "number of inter night angle filtered association": 0,
            },
        },
        {
            "old nid": 2,
            "old observation to tracklets report": {
                "number of inter night separation based association": 1,
                "number of inter night magnitude filtered association": 0,
                "number of inter night angle filtered association": 0,
                "number of duplicated association": 0,
                "metrics": {},
            },
            "old observation to new observation report": {
                "number of inter night separation based association": 0,
                "number of inter night magnitude filtered association": 0,
                "number of duplicated association": 0,
                "number of inter night angle filtered association": 0,
            },
        },
        {
            "old nid": 1,
            "old observation to tracklets report": {
                "number of inter night separation based association": 0,
                "number of inter night magnitude filtered association": 0,
                "number of inter night angle filtered association": 0,
                "number of duplicated association": 0,
                "metrics": {},
            },
            "old observation to new observation report": {
                "number of inter night separation based association": 1,
                "number of inter night magnitude filtered association": 0,
                "number of duplicated association": 0,
                "number of inter night angle filtered association": 0,
            },
        },
    ],
}

expected_traj_obs_report2 = {
    "list of updated trajectories": [6.0, 7.0, 8.0],
    "all nid report": [
        {
            "old nid": 3,
            "old observation to tracklets report": {
                "number of inter night separation based association": 0,
                "number of inter night magnitude filtered association": 0,
                "number of inter night angle filtered association": 0,
                "number of duplicated association": 0,
                "metrics": {},
            },
            "old observation to new observation report": {
                "number of inter night separation based association": 2,
                "number of inter night magnitude filtered association": 0,
                "number of duplicated association": 0,
                "number of inter night angle filtered association": 0,
            },
        },
        {
            "old nid": 2,
            "old observation to tracklets report": {
                "number of inter night separation based association": 0,
                "number of inter night magnitude filtered association": 0,
                "number of inter night angle filtered association": 0,
                "number of duplicated association": 0,
                "metrics": {},
            },
            "old observation to new observation report": {
                "number of inter night separation based association": 0,
                "number of inter night magnitude filtered association": 0,
                "number of duplicated association": 0,
                "number of inter night angle filtered association": 0,
            },
        },
        {
            "old nid": 1,
            "old observation to tracklets report": {
                "number of inter night separation based association": 0,
                "number of inter night magnitude filtered association": 0,
                "number of inter night angle filtered association": 0,
                "number of duplicated association": 0,
                "metrics": {},
            },
            "old observation to new observation report": {
                "number of inter night separation based association": 1,
                "number of inter night magnitude filtered association": 0,
                "number of duplicated association": 0,
                "number of inter night angle filtered association": 0,
            },
        },
    ],
}


expected_traj_obs_report3 = {
    "list of updated trajectories": [6.0, 7.0, 8.0, 11.0, 13.0],
    "all nid report": [
        {
            "old nid": 3,
            "old observation to tracklets report": {
                "number of inter night separation based association": 1,
                "number of inter night magnitude filtered association": 0,
                "number of inter night angle filtered association": 0,
                "number of duplicated association": 0,
                "metrics": {},
            },
            "old observation to new observation report": {
                "number of inter night separation based association": 2,
                "number of inter night magnitude filtered association": 0,
                "number of duplicated association": 0,
                "number of inter night angle filtered association": 0,
            },
        },
        {
            "old nid": 2,
            "old observation to tracklets report": {
                "number of inter night separation based association": 1,
                "number of inter night magnitude filtered association": 0,
                "number of inter night angle filtered association": 0,
                "number of duplicated association": 0,
                "metrics": {},
            },
            "old observation to new observation report": {
                "number of inter night separation based association": 0,
                "number of inter night magnitude filtered association": 0,
                "number of duplicated association": 0,
                "number of inter night angle filtered association": 0,
            },
        },
        {
            "old nid": 1,
            "old observation to tracklets report": {
                "number of inter night separation based association": 0,
                "number of inter night magnitude filtered association": 0,
                "number of inter night angle filtered association": 0,
                "number of duplicated association": 0,
                "metrics": {},
            },
            "old observation to new observation report": {
                "number of inter night separation based association": 1,
                "number of inter night magnitude filtered association": 0,
                "number of duplicated association": 0,
                "number of inter night angle filtered association": 0,
            },
        },
    ],
}

expected_traj_obs_report4 = {
    "list of updated trajectories": [11.0, 13.0],
    "all nid report": [
        {
            "old nid": 3,
            "old observation to tracklets report": {
                "number of inter night separation based association": 1,
                "number of inter night magnitude filtered association": 0,
                "number of inter night angle filtered association": 0,
                "number of duplicated association": 0,
                "metrics": {},
            },
            "old observation to new observation report": {
                "number of inter night separation based association": 0,
                "number of inter night magnitude filtered association": 0,
                "number of inter night angle filtered association": 0,
                "number of duplicated association": 0,
                "metrics": {},
            },
        },
        {
            "old nid": 2,
            "old observation to tracklets report": {
                "number of inter night separation based association": 1,
                "number of inter night magnitude filtered association": 0,
                "number of inter night angle filtered association": 0,
                "number of duplicated association": 0,
                "metrics": {},
            },
            "old observation to new observation report": {
                "number of inter night separation based association": 0,
                "number of inter night magnitude filtered association": 0,
                "number of inter night angle filtered association": 0,
                "number of duplicated association": 0,
                "metrics": {},
            },
        },
        {
            "old nid": 1,
            "old observation to tracklets report": {
                "number of inter night separation based association": 0,
                "number of inter night magnitude filtered association": 0,
                "number of inter night angle filtered association": 0,
                "number of duplicated association": 0,
                "metrics": {},
            },
            "old observation to new observation report": {
                "number of inter night separation based association": 0,
                "number of inter night magnitude filtered association": 0,
                "number of inter night angle filtered association": 0,
                "number of duplicated association": 0,
                "metrics": {},
            },
        },
    ],
}

# Night to night association testing

night_night_trajectory_sample = pd.DataFrame(
    {
        "ra": [1, 2, 3, 6, 7, 8, 11, 12, 13],
        "dec": [1, 2, 3, 1, 1, 2, 3, 4, 5],
        "dcmag": [12, 12.2, 12.4, 15, 15.4, 15.5, 13, 13.1, 13.2],
        "fid": [1, 1, 1, 1, 2, 2, 2, 2, 2],
        "nid": [1, 2, 3, 1, 2, 3, 1, 2, 3],
        "jd": [1, 2, 3, 1, 2, 3, 1, 2, 3],
        "candid": [10, 11, 12, 13, 14, 15, 16, 17, 18],
        "trajectory_id": [1, 1, 1, 2, 2, 2, 3, 3, 3],
    }
)

night_to_night_old_obs = pd.DataFrame(
    {
        "ra": [15, 7],
        "dec": [1, 7],
        "dcmag": [14, 16],
        "fid": [1, 2],
        "nid": [3, 2],
        "jd": [3, 2],
        "candid": [19, 29],
    }
)

night_to_night_new_obs = pd.DataFrame(
    {
        "ra": [4, 5, 1, 2, 12, 11, 16, 9, 17],
        "dec": [4, 5, 7, 8, 6, 7, 1, 3, 10],
        "dcmag": [12.5, 12.7, 17.2, 17.26, 13.32, 13.28, 14.12, 15.8, 15.21],
        "fid": [1, 1, 2, 2, 2, 2, 1, 1, 2],
        "nid": [4, 4, 4, 4, 4, 4, 4, 4, 4],
        "jd": [4.1, 4.2, 4.1, 4.2, 4.1, 4.2, 4.2, 4.1, 4.2],
        "candid": [20, 21, 22, 23, 24, 25, 26, 27, 28],
        "ssnamenr": [1, 1, 2, 2, 3, 3, 4, 5, 6],
    }
)


night_to_night_trajectory_df_expected = pd.DataFrame(
    {
        "ra": [1, 2, 3, 6, 7, 8, 11, 12, 13, 4, 5, 9, 15, 16, 1, 12, 2, 11],
        "dec": [1, 2, 3, 1, 1, 2, 3, 4, 5, 4, 5, 3, 1, 1, 7, 6, 8, 7],
        "dcmag": [
            12.00,
            12.20,
            12.40,
            15.00,
            15.40,
            15.50,
            13.00,
            13.10,
            13.20,
            12.50,
            12.70,
            15.80,
            14.00,
            14.12,
            17.20,
            13.32,
            17.26,
            13.28,
        ],
        "fid": [1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 2, 2, 2, 2],
        "nid": [1, 2, 3, 1, 2, 3, 1, 2, 3, 4, 4, 4, 3, 4, 4, 4, 4, 4],
        "jd": [
            1.0,
            2.0,
            3.0,
            1.0,
            2.0,
            3.0,
            1.0,
            2.0,
            3.0,
            4.1,
            4.2,
            4.1,
            3.0,
            4.2,
            4.1,
            4.1,
            4.2,
            4.2,
        ],
        "candid": [
            10,
            11,
            12,
            13,
            14,
            15,
            16,
            17,
            18,
            20,
            21,
            27,
            19,
            26,
            22,
            24,
            23,
            25,
        ],
        "trajectory_id": [1, 1, 1, 2, 2, 2, 3, 3, 3, 1, 1, 2, 7, 7, 5, 6, 5, 6],
        "ssnamenr": [
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            1,
            1,
            5,
            np.nan,
            4,
            2,
            3,
            2,
            3,
        ],
    }
)

night_to_night_old_observation_expected = pd.DataFrame(
    {
        "ra": [7, 17],
        "dec": [7, 10],
        "dcmag": [16.00, 15.21],
        "fid": [2, 2],
        "nid": [2, 4],
        "jd": [2.0, 4.2],
        "candid": [29, 28],
        "ssnamenr": [np.nan, 6.0],
    }
)


night_to_night_trajectory_df_expected2 = pd.DataFrame(
    {
        "ra": [15, 16, 4, 1, 12, 5, 2, 11],
        "dec": [1, 1, 4, 7, 6, 5, 8, 7],
        "dcmag": [14.00, 14.12, 12.50, 17.20, 13.32, 12.70, 17.26, 13.28],
        "fid": [1, 1, 1, 2, 2, 1, 2, 2],
        "nid": [3, 4, 4, 4, 4, 4, 4, 4],
        "jd": [3.0, 4.2, 4.1, 4.1, 4.1, 4.2, 4.2, 4.2],
        "candid": [19, 26, 20, 22, 24, 21, 23, 25],
        "trajectory_id": [7, 7, 4, 5, 6, 4, 5, 6],
        "ssnamenr": [np.nan, 4.0, 1, 2, 3, 1, 2, 3],
    }
)

night_to_night_old_observation_expected2 = pd.DataFrame(
    {
        "ra": [7, 9, 17],
        "dec": [7, 3, 10],
        "dcmag": [16.00, 15.80, 15.21],
        "fid": [2, 1, 2],
        "nid": [2, 4, 4],
        "jd": [2.0, 4.1, 4.2],
        "candid": [29, 27, 28],
        "ssnamenr": [np.nan, 5.0, 6.0],
    }
)


night_to_night_new_obs2 = pd.DataFrame(
    {
        "ra": [4, 5, 1, 2, 12, 11, 16, 9, 17],
        "dec": [4, 5, 7, 8, 6, 7, 1, 3, 10],
        "dcmag": [12.5, 17.7, 17.2, 13.26, 13.32, 18.28, 14.12, 15.8, 15.21],
        "fid": [1, 1, 2, 2, 2, 2, 1, 1, 2],
        "nid": [4, 4, 4, 4, 4, 4, 4, 4, 4],
        "jd": [4.1, 4.2, 4.1, 4.2, 4.1, 4.2, 4.2, 4.1, 4.2],
        "candid": [20, 21, 22, 23, 24, 25, 26, 27, 28],
    }
)


night_to_night_trajectory_df_expected3 = pd.DataFrame(
    {
        "ra": [
            1.0,
            2.0,
            3.0,
            6.0,
            7.0,
            8.0,
            11.0,
            12.0,
            13.0,
            4.0,
            9.0,
            15.0,
            16.0,
            7.0,
            5.0,
        ],
        "dec": [
            1.0,
            2.0,
            3.0,
            1.0,
            1.0,
            2.0,
            3.0,
            4.0,
            5.0,
            4.0,
            3.0,
            1.0,
            1.0,
            7.0,
            5.0,
        ],
        "dcmag": [
            12.00,
            12.20,
            12.40,
            15.00,
            15.40,
            15.50,
            13.00,
            13.10,
            13.20,
            12.50,
            15.80,
            14.00,
            14.12,
            16.00,
            17.70,
        ],
        "fid": [
            1.0,
            1.0,
            1.0,
            1.0,
            2.0,
            2.0,
            2.0,
            2.0,
            2.0,
            1.0,
            1.0,
            1.0,
            1.0,
            2.0,
            1.0,
        ],
        "nid": [
            1.0,
            2.0,
            3.0,
            1.0,
            2.0,
            3.0,
            1.0,
            2.0,
            3.0,
            4.0,
            4.0,
            3.0,
            4.0,
            2.0,
            4.0,
        ],
        "jd": [
            1.0,
            2.0,
            3.0,
            1.0,
            2.0,
            3.0,
            1.0,
            2.0,
            3.0,
            4.1,
            4.1,
            3.0,
            4.2,
            2.0,
            4.2,
        ],
        "candid": [10, 11, 12, 13, 14, 15, 16, 17, 18, 20, 27, 19, 26, 29, 21],
        "trajectory_id": [1, 1, 1, 2, 2, 2, 3, 3, 3, 1, 2, 4, 4, 5, 5],
    }
)

night_to_night_old_observation_expected3 = pd.DataFrame(
    {
        "ra": [1, 2, 12, 11, 17],
        "dec": [7, 8, 6, 7, 10],
        "dcmag": [17.20, 13.26, 13.32, 18.28, 15.21],
        "fid": [2, 2, 2, 2, 2],
        "nid": [4, 4, 4, 4, 4],
        "jd": [4.1, 4.2, 4.1, 4.2, 4.2],
        "candid": [22, 23, 24, 25, 28],
    }
)

inter_night_report1 = {
    "nid of the next night": 4,
    "intra night report": {
        "number of separation association": 6,
        "number of association filtered by magnitude": 0,
        "association metrics": {
            "precision": 100.0,
            "recall": 100.0,
            "True Positif": 3,
            "False Positif": 0,
            "False Negatif": 0,
            "total real association": 3,
        },
        "number of intra night tracklets": 3,
    },
    "trajectory association report": {
        "list of updated trajectories": [1.0, 2.0],
        "all nid report": [
            {
                "old nid": 3,
                "trajectories_to_tracklets_report": {
                    "number of inter night separation based association": 2,
                    "number of inter night magnitude filtered association": 0,
                    "number of inter night angle filtered association": 1,
                    "number of duplicated association": 0,
                    "metrics": {},
                },
                "trajectories_to_new_observation_report": {
                    "number of inter night separation based association": 1,
                    "number of inter night magnitude filtered association": 0,
                    "number of inter night angle filtered association": 0,
                    "number of duplicated association": 0,
                    "metrics": {},
                },
            }
        ],
    },
    "tracklets and observation association report": {
        "list of updated trajectories": [5.0, 6.0, 7.0],
        "all nid report": [
            {
                "old nid": 3,
                "old observation to tracklets report": {
                    "number of inter night separation based association": 0,
                    "number of inter night magnitude filtered association": 0,
                    "number of inter night angle filtered association": 0,
                    "number of duplicated association": 0,
                    "metrics": {},
                },
                "old observation to new observation report": {
                    "number of inter night separation based association": 1,
                    "number of inter night magnitude filtered association": 0,
                    "metrics": {},
                    "number of duplicated association": 0,
                    "number of inter night angle filtered association": 0,
                },
            },
            {
                "old nid": 2,
                "old observation to tracklets report": {
                    "number of inter night separation based association": 0,
                    "number of inter night magnitude filtered association": 0,
                    "number of inter night angle filtered association": 0,
                    "number of duplicated association": 0,
                    "metrics": {},
                },
                "old observation to new observation report": {
                    "number of inter night separation based association": 0,
                    "number of inter night magnitude filtered association": 0,
                    "metrics": {},
                    "number of duplicated association": 0,
                    "number of inter night angle filtered association": 0,
                },
            },
        ],
    },
}

inter_night_report2 = {
    "nid of the next night": 4,
    "intra night report": {
        "number of separation association": 6,
        "number of association filtered by magnitude": 0,
        "association metrics": {},
        "number of intra night tracklets": 3,
    },
    "trajectory association report": {
        "list of updated trajectories": [],
        "all nid report": [],
    },
    "tracklets and observation association report": {
        "list of updated trajectories": [4.0, 5.0, 6.0, 7.0],
        "all nid report": [
            {
                "old nid": 3,
                "old observation to tracklets report": {
                    "number of inter night separation based association": 0,
                    "number of inter night magnitude filtered association": 0,
                    "number of inter night angle filtered association": 0,
                    "number of duplicated association": 0,
                    "metrics": {},
                },
                "old observation to new observation report": {
                    "number of inter night separation based association": 1,
                    "number of inter night magnitude filtered association": 0,
                    "number of duplicated association": 0,
                    "number of inter night angle filtered association": 0,
                },
            },
            {
                "old nid": 2,
                "old observation to tracklets report": {
                    "number of inter night separation based association": 0,
                    "number of inter night magnitude filtered association": 0,
                    "number of inter night angle filtered association": 0,
                    "number of duplicated association": 0,
                    "metrics": {},
                },
                "old observation to new observation report": {
                    "number of inter night separation based association": 0,
                    "number of inter night magnitude filtered association": 0,
                    "number of duplicated association": 0,
                    "number of inter night angle filtered association": 0,
                },
            },
        ],
    },
}

inter_night_report3 = {
    "nid of the next night": 4,
    "intra night report": {
        "number of separation association": 6,
        "number of association filtered by magnitude": 6,
        "association metrics": {},
        "number of intra night tracklets": 0,
    },
    "trajectory association report": {
        "list of updated trajectories": [1.0, 2.0],
        "all nid report": [
            {
                "old nid": 3,
                "trajectories_to_tracklets_report": {
                    "number of inter night separation based association": 0,
                    "number of inter night magnitude filtered association": 0,
                    "number of inter night angle filtered association": 0,
                    "number of duplicated association": 0,
                    "metrics": {},
                },
                "trajectories_to_new_observation_report": {
                    "number of inter night separation based association": 3,
                    "number of inter night magnitude filtered association": 0,
                    "number of inter night angle filtered association": 1,
                    "number of duplicated association": 0,
                    "metrics": {},
                },
            }
        ],
    },
    "tracklets and observation association report": {
        "list of updated trajectories": [4.0, 5.0],
        "all nid report": [
            {
                "old nid": 3,
                "old observation to tracklets report": {
                    "number of inter night separation based association": 0,
                    "number of inter night magnitude filtered association": 0,
                    "number of inter night angle filtered association": 0,
                    "number of duplicated association": 0,
                    "metrics": {},
                },
                "old observation to new observation report": {
                    "number of inter night separation based association": 1,
                    "number of inter night magnitude filtered association": 0,
                    "number of duplicated association": 0,
                    "number of inter night angle filtered association": 0,
                },
            },
            {
                "old nid": 2,
                "old observation to tracklets report": {
                    "number of inter night separation based association": 0,
                    "number of inter night magnitude filtered association": 0,
                    "number of inter night angle filtered association": 0,
                    "number of duplicated association": 0,
                    "metrics": {},
                },
                "old observation to new observation report": {
                    "number of inter night separation based association": 1,
                    "number of inter night magnitude filtered association": 0,
                    "number of duplicated association": 0,
                    "number of inter night angle filtered association": 0,
                },
            },
        ],
    },
}


# Trajectory and tracklets association test

trajectories_sample_1 = pd.DataFrame(
    {
        "ra": [1, 2, 3, 5, 6, 6, 1, 2, 3, 7, 8, 8, 9, 10, 11, 11],
        "dec": [1, 2, 3, 1, 1, 2, 7, 7, 7, 4, 5, 6, 1, 1, 1, 2],
        "dcmag": [
            12,
            12.02,
            12.04,
            13,
            13.02,
            13.04,
            14,
            14.02,
            14.04,
            15.04,
            15.06,
            15.07,
            16.02,
            16.04,
            16.06,
            16.07,
        ],
        "fid": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        "nid": [0, 0, 0, 1, 1, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 2],
        "jd": [
            0.1,
            0.2,
            0.3,
            1.1,
            1.2,
            1.3,
            2.1,
            2.2,
            2.3,
            1.1,
            1.2,
            1.3,
            1.1,
            1.2,
            1.3,
            2.1,
        ],
        "candid": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
        "trajectory_id": [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 4],
    }
)

tracklets_sample_1 = pd.DataFrame(
    {
        "ra": [4, 5, 8, 8, 11, 11, 11, 7, 8],
        "dec": [4, 5, 7, 8, 3, 4, 5, 3, 3],
        "dcmag": [12.06, 12.07, 15.08, 15.09, 16.08, 16.09, 16.11, 17.01, 17.02],
        "fid": [1, 1, 1, 1, 1, 1, 1, 1, 1],
        "nid": [3, 3, 3, 3, 3, 3, 3, 3, 3],
        "jd": [3.1, 3.2, 3.1, 3.2, 3.1, 3.2, 3.3, 3.4, 3.5],
        "candid": [16, 17, 18, 19, 20, 21, 22, 23, 24],
        "trajectory_id": [10, 10, 11, 11, 12, 12, 12, 13, 13],
    }
)

trajectories_expected_1 = pd.DataFrame(
    {
        "ra": [1, 2, 3, 1, 2, 2, 6, 7, 8, 6, 7, 8, 9, 10, 10, 4, 5, 8, 7],
        "dec": [1, 2, 3, 12, 11, 10, 12, 12, 12, 6, 5, 6, 1, 2, 3, 4, 5, 7, 8],
        "dcmag": [
            12.02,
            12.05,
            12.3,
            15.0,
            15.1,
            15.23,
            13.0,
            12.6,
            12.75,
            17.02,
            17.15,
            17.27,
            16.0,
            16.4,
            16.7,
            12.4,
            12.52,
            17.31,
            17.43,
        ],
        "fid": [1, 1, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 1, 1, 1, 1, 1],
        "nid": [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 4, 4, 4, 4],
        "jd": [
            1.0,
            2.0,
            3.0,
            1.0,
            2.0,
            3.0,
            1.0,
            2.0,
            3.0,
            1.0,
            2.0,
            3.0,
            1.0,
            2.0,
            3.0,
            4.1,
            4.2,
            4.1,
            4.2,
        ],
        "candid": [
            10,
            11,
            12,
            13,
            14,
            15,
            16,
            17,
            18,
            19,
            20,
            21,
            22,
            23,
            24,
            25,
            26,
            29,
            30,
        ],
        "trajectory_id": [
            1.0,
            1.0,
            1.0,
            2.0,
            2.0,
            2.0,
            3.0,
            3.0,
            3.0,
            4.0,
            4.0,
            4.0,
            5.0,
            5.0,
            5.0,
            1.0,
            1.0,
            4.0,
            4.0,
        ],
        "not_updated": [
            False,
            False,
            False,
            True,
            True,
            True,
            True,
            True,
            True,
            False,
            False,
            False,
            True,
            True,
            True,
            False,
            False,
            False,
            False,
        ],
    }
)

tracklets_expected_1 = pd.DataFrame(
    {
        "ra": [1, 1, 13, 13],
        "dec": [9, 8, 1, 2],
        "dcmag": [15.94, 15.47, 16.21, 16.28],
        "fid": [2, 1, 2, 2],
        "nid": [4, 4, 4, 4],
        "jd": [4.1, 4.2, 4.1, 4.2],
        "candid": [27, 28, 31, 32],
        "trajectory_id": [11, 11, 13, 13],
    }
)

trajectories_expected_2 = pd.DataFrame(
    {
        "ra": [
            1,
            2,
            3,
            5,
            6,
            6,
            1,
            2,
            3,
            7,
            8,
            8,
            9,
            10,
            11,
            11,
            11,
            11,
            11,
            8,
            8,
            4,
            5,
        ],
        "dec": [1, 2, 3, 1, 1, 2, 7, 7, 7, 4, 5, 6, 1, 1, 1, 2, 3, 4, 5, 7, 8, 4, 5],
        "dcmag": [
            12.0,
            12.02,
            12.04,
            13.0,
            13.02,
            13.04,
            14.0,
            14.02,
            14.04,
            15.04,
            15.06,
            15.07,
            16.02,
            16.04,
            16.06,
            16.07,
            16.08,
            16.09,
            16.11,
            15.08,
            15.09,
            12.06,
            12.07,
        ],
        "fid": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        "nid": [0, 0, 0, 1, 1, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 2, 3, 3, 3, 3, 3, 3, 3],
        "jd": [
            0.1,
            0.2,
            0.3,
            1.1,
            1.2,
            1.3,
            2.1,
            2.2,
            2.3,
            1.1,
            1.2,
            1.3,
            1.1,
            1.2,
            1.3,
            2.1,
            3.1,
            3.2,
            3.3,
            3.1,
            3.2,
            3.1,
            3.2,
        ],
        "candid": [
            0,
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            20,
            21,
            22,
            18,
            19,
            16,
            17,
        ],
        "trajectory_id": [
            0.0,
            0.0,
            0.0,
            1.0,
            1.0,
            1.0,
            2.0,
            2.0,
            2.0,
            3.0,
            3.0,
            3.0,
            4.0,
            4.0,
            4.0,
            4.0,
            4.0,
            4.0,
            4.0,
            3.0,
            3.0,
            0.0,
            0.0,
        ],
        "not_updated": [
            False,
            False,
            False,
            True,
            True,
            True,
            True,
            True,
            True,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
        ],
    }
)

tracklets_expected_2 = pd.DataFrame(
    {
        "ra": [7, 8],
        "dec": [3, 3],
        "dcmag": [17.01, 17.02],
        "fid": [1, 1],
        "nid": [3, 3],
        "jd": [3.4, 3.5],
        "candid": [23, 24],
        "trajectory_id": [13, 13],
    }
)

traj_and_track_assoc_report_expected = {
    "updated trajectories": [0.0, 3.0, 4.0],
    "all nid_report": [
        {
            "old nid": 2,
            "trajectories_to_tracklets_report": {
                "number of inter night separation based association": 2,
                "number of inter night magnitude filtered association": 1,
                "number of inter night angle filtered association": 0,
                "number of duplicated association": 0,
                "metrics": {},
            },
        },
        {
            "old nid": 1,
            "trajectories_to_tracklets_report": {
                "number of inter night separation based association": 1,
                "number of inter night magnitude filtered association": 0,
                "number of inter night angle filtered association": 0,
                "number of duplicated association": 0,
                "metrics": {},
            },
        },
        {
            "old nid": 0,
            "trajectories_to_tracklets_report": {
                "number of inter night separation based association": 2,
                "number of inter night magnitude filtered association": 1,
                "number of inter night angle filtered association": 0,
                "number of duplicated association": 0,
                "metrics": {},
            },
        },
    ],
}
