import astropy.units as u
from astropy.coordinates import SkyCoord
import pandas as pd
import numpy as np

from alert_association.intra_night_association import magnitude_association
from alert_association.intra_night_association import (
    get_n_last_observations_from_trajectories,
)
from alert_association.intra_night_association import compute_inter_night_metric


def night_to_night_separation_association(
    old_observation, new_observation, separation_criterion
):
    """
    Perform night-night association based on the separation between the alerts.
    The separation criterion was computed by a data analysis on the MPC object.

    Parameters
    ----------
    old_observation : dataframe
        observation of night t-1
    new_observation : dataframe
        observation of night t
    separation_criterion : float
        the separation limit between the alerts to be associated, must be in arcsecond

    Returns
    -------
    left_assoc : dataframe
        Associations are a binary relation with left members and right members, return the left members (from old_observation) of the associations
    right_assoc : dataframe
        return right members (from new_observation) of the associations
    sep2d : list
        return the separation between the associated alerts

    Examples
    --------
    >>> test_night1 = pd.DataFrame({
    ... 'ra': [10, 11, 20],
    ... 'dec' : [70, 30, 50],
    ... 'candid' : [1, 2, 3],
    ... 'trajectory_id' : [10, 11, 12]
    ... })

    >>> test_night2 = pd.DataFrame({
    ... 'ra' : [11, 12, 21],
    ... 'dec' : [69, 29, 49],
    ... 'candid' : [4, 5, 6],
    ... 'trajectory_id' : [10, 11, 12]
    ... })

    >>> left, right, sep = night_to_night_separation_association(test_night1, test_night2, 2*u.degree)

    >>> assert_frame_equal(test_night1, left)
    >>> assert_frame_equal(test_night2, right)
    >>> np.any([1.05951524, 1.32569856, 1.19235978] == np.around(sep.value, 8))
    True
    """

    old_observations_coord = SkyCoord(
        old_observation["ra"], old_observation["dec"], unit=u.degree
    )
    new_observations_coord = SkyCoord(
        new_observation["ra"], new_observation["dec"], unit=u.degree
    )

    new_obs_idx, old_obs_idx, sep2d, _ = old_observations_coord.search_around_sky(
        new_observations_coord, separation_criterion
    )

    old_obs_assoc = old_observation.iloc[old_obs_idx]
    new_obs_assoc = new_observation.iloc[new_obs_idx]
    return old_obs_assoc, new_obs_assoc, sep2d


def angle_three_point(a, b, c):
    """
    Compute the angle between three points taken as two vectors

    Parameters
    ----------
    a : numpy array
        first point
    b : numpy array
        second point
    c : numpy array
        third point

    Returns
    -------
    angle : float
        the angle formed by the three points

    Examples
    --------
    >>> a = np.array([1, 1])
    >>> b = np.array([3, 2])
    >>> c = np.array([5, 4])

    >>> np.around(angle_three_point(a, b, c), 3)
    10.305

    >>> c = np.array([-2, -2])
    >>> np.around(angle_three_point(a, b, c), 3)
    161.565
    """
    ba = b - a
    ca = c - a

    cosine_angle = np.dot(ba, ca) / (np.linalg.norm(ba) * np.linalg.norm(ca))
    angle = np.arccos(cosine_angle)

    return np.degrees(angle)


def angle_df(x):
    """
    Taken three alerts from a dataframe rows, computes the angle between the three alerts

    Parameters
    x : dataframe rows
        a rows from a dataframe with the three consecutives alerts to compute the angle.


    Returns
    -------
    res_angle : float
        the angle between the three consecutives alerts normalized by the jd difference between the second point and the third point.

    Examples
    --------
    >>> from pandera import Check, Column, DataFrameSchema

    >>> df_schema = DataFrameSchema({
    ... "trajectory_id": Column(int),
    ... "ra_x": Column(object),
    ... "dec_x": Column(object),
    ... "jd_x": Column(object),
    ... "candid": Column(int),
    ... "index": Column(int),
    ... "ra_y": Column(float),
    ... "dec_y": Column(float),
    ... "jd_y": Column(float)
    ... })

    >>> test_dataframe = pd.DataFrame({
    ... 'trajectory_id': [0],
    ... 'ra_x': [[1, 3]],
    ... 'dec_x': [[1, 2]],
    ... 'jd_x': [[0, 1]],
    ... 'candid': [0],
    ... 'index' : [0],
    ... 'ra_y': [5.0],
    ... 'dec_y':[4.0],
    ... 'jd_y': [2.0]
    ... })

    >>> test_dataframe = df_schema.validate(test_dataframe)

    >>> res = test_dataframe.apply(angle_df, axis=1)

    >>> np.around(np.array(res)[0], 3)
    10.305
    """

    ra_x, dec_x, jd_x = x[1], x[2], x[3]

    ra_y, dec_y, jd_y = x[6], x[7], x[8]

    a = np.array([ra_x[0], dec_x[0]])
    b = np.array([ra_x[1], dec_x[1]])
    c = np.array([ra_y, dec_y])

    jd_x = jd_x[1]

    diff_jd = jd_y - jd_x

    if diff_jd > 1:
        res_angle = angle_three_point(a, b, c) / diff_jd
    else:
        res_angle = angle_three_point(a, b, c)

    return res_angle


def cone_search_association(
    two_last_observations, traj_assoc, new_obs_assoc, angle_criterion
):
    """
    Filter the association based on a cone search. The idea is to remove the alerts triplets that have an angle greater than the angle_criterion.

    Parameters
    ----------
    two_last_observations : dataframe
        a dataframe that contains the two last observations for each trajectories
    traj_assoc : dataframe
        a dataframe which contains the trajectories extremity that are associated with the new observations.
        The trajectory extremity in traj_assoc have to be in two_last_observations.
    new_obs_assoc : dataframe
        new observations that will be associated with the trajectories extremity represented by the two last observations.
    angle_criterion : float
        the angle limit between the three points formed by the two last observation and the new observations to associates.

    Returns
    -------
    traj_assoc : dataframe
        trajectories extremity associated with the new observations filtered by the angle cone search
    new_obs_assoc : dataframe
        new observations associated with the trajectories filtered by the angle cone search

    Examples
    --------
    >>> left, right = cone_search_association(ts.cone_search_two_last_observation_sample, ts.traj_assoc_sample, ts.new_obs_assoc_sample, 8.8)

    >>> assert_frame_equal(left, ts.left_cone_search_expected)
    >>> assert_frame_equal(right, ts.right_cone_search_expected)

    >>> left, right = cone_search_association(ts.false_cone_search_two_last_observation_sample, ts.false_traj_assoc_sample, ts.false_new_obs_assoc_sample, 8.8)

    >>> left_expected = pd.DataFrame(columns = ['ra', 'dec', 'jd', 'candid', 'trajectory_id'])
    >>> right_expected = pd.DataFrame(columns = ['ra', 'dec', 'jd', 'candid', 'tmp_traj', 'trajectory_id'])

    >>> assert_frame_equal(left, left_expected, check_index_type=False, check_dtype=False)
    >>> assert_frame_equal(right, right_expected, check_index_type=False, check_dtype=False)
    """

    # reset the index of the associated members in order to recovered the right rows after the angle filters.
    traj_assoc = traj_assoc.reset_index(drop=True).reset_index()
    new_obs_assoc = new_obs_assoc.reset_index(drop=True).reset_index()

    # rename the new trajectory_id column to another name in order to give the trajectory_id of the associated trajectories
    # and keep the new trajectory_id
    new_obs_assoc = new_obs_assoc.rename({"trajectory_id": "tmp_traj"}, axis=1)
    new_obs_assoc["trajectory_id"] = traj_assoc["trajectory_id"]

    # get the two last observations of the associated trajectories in order to compute the cone search angle
    two_last = two_last_observations[
        two_last_observations["trajectory_id"].isin(traj_assoc["trajectory_id"])
    ]

    # groupby the two last observations in order to prepare the merge with the new observations
    two_last = two_last.groupby(["trajectory_id"]).agg(
        {"ra": list, "dec": list, "jd": list, "candid": lambda x: len(x)}
    )

    # merge the two last observation with the new observations to be associated
    prep_angle = two_last.merge(
        new_obs_assoc[["index", "ra", "dec", "jd", "trajectory_id"]], on="trajectory_id"
    )

    # compute the cone search angle
    prep_angle["angle"] = prep_angle.apply(angle_df, axis=1)

    # filter by the physical properties angle
    remain_assoc = prep_angle[prep_angle["angle"] <= angle_criterion]

    # keep only the alerts that match with the angle filter
    traj_assoc = traj_assoc.loc[remain_assoc["index"].values]
    new_obs_assoc = new_obs_assoc.loc[remain_assoc["index"].values]

    return traj_assoc.drop(["index"], axis=1), new_obs_assoc.drop(["index"], axis=1)


def night_to_night_observation_association(
    obs_set1, obs_set2, sep_criterion, mag_criterion_same_fid, mag_criterion_diff_fid
):
    """
    Night to night associations between the observations

    Parameters
    ----------
    obs_set1 : dataframe
        first set of observations (typically, the oldest observations)
    obs_set2 : dataframe
        second set of observations (typically, the newest observations)
    sep_criterion : float
        the separation criterion to associates alerts
    mag_criterion_same_fid : float
        the magnitude criterion to associates alerts if the observations have been observed with the same filter
    mag_criterion_diff_fid : float
        the magnitude criterion to associates alerts if the observations have been observed with the same filter

    Returns
    -------
    traj_assoc : dataframe
        the left members of the associations, can be an extremity of a trajectory
    new_obs_assoc : dataframe
        new observations to add to the associated trajectories
    inter_night_obs_assoc_report : dictionary
        statistics about the observation association process, contains the following entries :

                    number of inter night separation based association

                    number of inter night magnitude filtered association

    Examples
    --------

    >>> night_1 = pd.DataFrame({
    ... "ra": [1, 1, 4, 6, 10],
    ... "dec": [1, 8, 4, 7, 2],
    ... "dcmag": [13, 15, 14, 16, 12],
    ... "fid": [1, 2, 1, 2, 2],
    ... "jd": [1, 1, 1, 1, 1],
    ... "candid": [10, 11, 12, 13, 14]
    ... })

    >>> night_2 = pd.DataFrame({
    ... "ra": [2, 6, 5, 7, 7, 8],
    ... "dec": [2, 4, 3, 10, 7, 3],
    ... "dcmag": [13.05, 17, 14.09, 18, 13, 16.4],
    ... "fid": [1, 2, 2, 2, 1, 1],
    ... "jd": [2, 2, 2, 2, 2, 2],
    ... "candid": [15, 16, 17, 18, 19, 20]
    ... })

    >>> left, right, report = night_to_night_observation_association(night_1, night_2, 1.5 * u.degree, 0.2, 0.5)

    >>> expected_report = {'number of inter night separation based association': 3, 'number of inter night magnitude filtered association': 1}

    >>> left_expected = pd.DataFrame({
    ... "ra": [1, 4],
    ... "dec": [1, 4],
    ... "dcmag": [13, 14],
    ... "fid": [1, 1],
    ... "jd": [1, 1],
    ... "candid": [10, 12]
    ... })

    >>> right_expected = pd.DataFrame({
    ... "ra": [2, 5],
    ... "dec": [2, 3],
    ... "dcmag": [13.05, 14.09],
    ... "fid": [1, 2],
    ... "jd": [2, 2],
    ... "candid": [15, 17]
    ... })

    >>> assert_frame_equal(left.reset_index(drop=True), left_expected)
    >>> assert_frame_equal(right.reset_index(drop=True), right_expected)
    >>> TestCase().assertDictEqual(expected_report, report)
    """

    inter_night_obs_assoc_report = dict()

    # association based separation
    traj_assoc, new_obs_assoc, sep = night_to_night_separation_association(
        obs_set1, obs_set2, sep_criterion
    )

    inter_night_obs_assoc_report[
        "number of inter night separation based association"
    ] = len(new_obs_assoc)

    # filter the association based on magnitude criterion
    traj_assoc, new_obs_assoc = magnitude_association(
        traj_assoc,
        new_obs_assoc,
        mag_criterion_same_fid,
        mag_criterion_diff_fid,
        jd_normalization=True,
    )

    inter_night_obs_assoc_report[
        "number of inter night magnitude filtered association"
    ] = inter_night_obs_assoc_report[
        "number of inter night separation based association"
    ] - len(
        new_obs_assoc
    )

    return traj_assoc, new_obs_assoc, inter_night_obs_assoc_report


def night_to_night_trajectory_associations(
    two_last_observations,
    observations_to_associates,
    sep_criterion,
    mag_criterion_same_fid,
    mag_criterion_diff_fid,
    angle_criterion,
):
    """
    Associates the extremity of the trajectories with the new observations. The new observations can be a single observations or the extremity of a trajectories.

    Parameters
    ----------
    two_last_observation : dataframe
        the two last observations of the trajectories used to compute the angle for the cone search filtering. The last observations is also used
        to perform the search around sky.
    observations_to_associates : dataframe
        The observations to associates with the extremity of the trajectories. These observations can be single or the extremity of another trajectories.
    sep_criterion : float
        the separation criterion to associates alerts
    mag_criterion_same_fid : float
        the magnitude criterion to associates alerts if the observations have been observed with the same filter
    mag_criterion_diff_fid : float
        the magnitude criterion to associates alerts if the observations have been observed with the same filter
    angle_criterion : float
        the angle criterion to associates alerts during the cone search

    Returns
    -------
    traj_assoc : dataframe
        the left members of the associations, extremity of the trajectories
    new_obs_assoc : dataframe
        new observations to add to the associated trajectories
    inter_night_obs_report : dictionary
        statistics about the trajectory association process, contains the following entries :

                    number of inter night separation based association

                    number of inter night magnitude filtered association

                    number of inter night angle filtered association

    Examples
    --------
    >>> left, right, report = night_to_night_trajectory_associations(ts.night_to_night_two_last_sample, ts.night_to_night_new_observation, 2 * u.degree, 0.2, 0.5, 30)

    >>> expected_report = {'number of inter night separation based association': 6, 'number of inter night magnitude filtered association': 1, 'number of inter night angle filtered association': 1}

    >>> assert_frame_equal(left.reset_index(drop=True), ts.night_to_night_traj_assoc_left_expected)
    >>> assert_frame_equal(right.reset_index(drop=True), ts.night_to_night_traj_assoc_right_expected)
    >>> TestCase().assertDictEqual(expected_report, report)
    """
    # get the last observations of the trajectories to perform the associations
    last_traj_obs = (
        two_last_observations.groupby(["trajectory_id"]).last().reset_index()
    )

    (
        traj_assoc,
        new_obs_assoc,
        inter_night_obs_report,
    ) = night_to_night_observation_association(
        last_traj_obs,
        observations_to_associates,
        sep_criterion,
        mag_criterion_same_fid,
        mag_criterion_diff_fid,
    )

    nb_assoc_before_angle_filtering = len(new_obs_assoc)
    inter_night_obs_report["number of inter night angle filtered association"] = 0
    if len(traj_assoc) != 0:

        traj_assoc, new_obs_assoc = cone_search_association(
            two_last_observations, traj_assoc, new_obs_assoc, angle_criterion
        )

        inter_night_obs_report[
            "number of inter night angle filtered association"
        ] = nb_assoc_before_angle_filtering - len(new_obs_assoc)

        return traj_assoc, new_obs_assoc, inter_night_obs_report
    else:
        return traj_assoc, new_obs_assoc, inter_night_obs_report


# The two functions below are used if we decide to manage the multiple associations that can appears during the process.
# They are not yet used.
def assign_new_trajectory_id_to_new_tracklets(
    new_obs, traj_next_night
):  # pragma: no cover
    """
    Propagate the trajectory id of the new obs to all observations of the corresponding trajectory

    Parameters
    ----------
    new_obs : dataframe
        the new observations that will be associated with a trajectory
    traj_next_night : dataframe
        dataframe that contains all the tracklets of the next night.

    Returns
    -------
    traj_next_night : dataframe
        all tracklets without the ones where new_obs appears.
    all_tracklets : dataframe
        all tracklets where new_obs appears
    """
    all_tracklets = []
    for _, rows in new_obs.iterrows():
        traj_id = rows["tmp_traj"]

        # get all the alerts associated with this first observations
        mask = traj_next_night.trajectory_id.apply(
            lambda x: any(i == traj_id for i in x)
        )
        multi_traj = traj_next_night[mask.values]

        # change the trajectory_id of the associated alerts with the original trajectory_id of the associated trajectory
        multi_traj["trajectory_id"] = [
            [rows["trajectory_id"]] for _ in range(len(multi_traj))
        ]
        all_tracklets.append(multi_traj)

        # remove the associated tracklets
        traj_next_night = traj_next_night[~mask]

    return traj_next_night, pd.concat(all_tracklets)


def tracklets_id_management(
    traj_left, traj_right, traj_next_night, trajectory_df
):  # pragma: no cover
    """
    This functions perform the trajectory_id propagation between the already known trajectory and the new tracklets that will be associates.

    This function remove also the tracklets involved in an association in traj_next_night and update trajectory_df with all tracklets involved in an associations.

    Parameters
    ----------
    traj_left : dataframe
        the trajectories extremity
    traj_right : dataframe
        the tracklets extremity
    traj_next_night : dataframe
        the tracklets observations without the tracklets extremity
    trajectory_id : dataframe
        all the observation involved in the predict trajectories.

    Returns
    -------
    trajectory_df : dataframe
        the trajectory_df updated with the new tracklets associated with a new trajectory.
    traj_next_night : dataframe
        the remain tracklets that have not been associate with a trajectory.
    """
    traj_left = traj_left.reset_index(drop=True).reset_index()
    traj_right = traj_right.reset_index(drop=True)

    # detect the multiple associations with the left members (trajectories)
    multiple_assoc = traj_left.groupby(["trajectory_id"]).agg(
        {"index": list, "candid": lambda x: len(x)}
    )

    # get the associations not involved in a multiple associations
    single_assoc = traj_right.loc[
        multiple_assoc[multiple_assoc["candid"] == 1].explode(["index"])["index"].values
    ]

    # get the tracklets extremity involved in the multiple associations
    multiple_obs = traj_right.loc[
        multiple_assoc[multiple_assoc["candid"] > 1].explode(["index"])["index"].values
    ]

    first_occur = (
        first_occur_tracklets
    ) = other_occur = other_occurs_tracklets = pd.DataFrame()

    if len(multiple_obs) > 0:
        # get the first occurence in the multiple associations
        first_occur = multiple_obs[multiple_obs.duplicated(["trajectory_id"])]

        # get the others occurences
        other_occur = multiple_obs[~multiple_obs.duplicated(["trajectory_id"])]

        all_other_occur_tracklets = []
        # add the trajectory_id of the all other occurences to the list of trajectory_id of the associated trajectories
        for _, rows in other_occur.iterrows():
            traj_id = rows["trajectory_id"]

            # get all rows of the associated trajectory
            mask = trajectory_df.trajectory_id.apply(
                lambda x: any(i == traj_id for i in x)
            )
            multi_traj = trajectory_df[mask]

            # get the trajectory id list of the associated trajectory
            multi_traj_id = multi_traj["trajectory_id"].values
            # duplicates the new trajectory_id which will be added to the trajectory id list
            new_traj_id = [[rows["tmp_traj"]] for _ in range(len(multi_traj))]

            # concatenate the trajectory id list with the new trajectory id and add this new list to the trajectory_id columns of the associated trajectory
            trajectory_df.loc[multi_traj.index.values, "trajectory_id"] = [
                el1 + el2 for el1, el2 in zip(multi_traj_id, new_traj_id)
            ]

            # get all rows of the associated tracklets of the next night
            mask = traj_next_night.trajectory_id.apply(
                lambda x: any(i == rows["tmp_traj"] for i in x)
            )
            next_night_tracklets = traj_next_night[mask]
            all_other_occur_tracklets.append(next_night_tracklets)

            # remove the associated tracklets
            traj_next_night = traj_next_night[~mask]

        other_occurs_tracklets = pd.concat(all_other_occur_tracklets)
        (
            traj_next_night,
            first_occur_tracklets,
        ) = assign_new_trajectory_id_to_new_tracklets(first_occur, traj_next_night)
        other_occur = other_occur.drop(["trajectory_id"], axis=1).rename(
            {"tmp_traj": "trajectory_id"}, axis=1
        )
        first_occur = first_occur.drop(["tmp_traj"], axis=1)
        first_occur["trajectory_id"] = [
            [el] for el in first_occur["trajectory_id"].values
        ]
        other_occur["trajectory_id"] = [
            [el] for el in other_occur["trajectory_id"].values
        ]

    traj_next_night, single_assoc_tracklets = assign_new_trajectory_id_to_new_tracklets(
        single_assoc, traj_next_night
    )
    single_assoc["trajectory_id"] = [
        [el] for el in single_assoc["trajectory_id"].values
    ]
    # add all the new tracklets in the trajectory dataframe with the right trajectory_id
    # return also all the tracklets without those added in the trajectory dataframe
    all_df_to_concat = [
        trajectory_df,
        first_occur,
        first_occur_tracklets,
        other_occur,
        other_occurs_tracklets,
        single_assoc.drop(["tmp_traj"], axis=1),
        single_assoc_tracklets,
    ]

    return pd.concat(all_df_to_concat), traj_next_night


def trajectory_associations(
    trajectory_df,
    traj_next_night,
    new_observations,
    sep_criterion,
    mag_criterion_same_fid,
    mag_criterion_diff_fid,
    angle_criterion,
    run_metrics=False,
):
    """
    Perform the trajectory association process. Firstly, associate the recorded trajectories with the tracklets from the new nights.
    Secondly, associate the remaining recorded trajectories with the observations from the new night that not occurs in the tracklets.

    Parameters
    ----------
    trajectory_df : dataframe
        the recorded trajectory generate by the linkage algorithm
    traj_next_night : dataframe
        the tracklets from the new night
    new_observations : dataframe
        new observations from the new night. not included in traj_next_night
    sep_criterion : float
        the separation criterion to associates alerts
    mag_criterion_same_fid : float
        the magnitude criterion to associates alerts if the observations have been observed with the same filter
    mag_criterion_diff_fid : float
        the magnitude criterion to associates alerts if the observations have been observed with the same filter
    angle_criterion : float
        the angle criterion to associates alerts during the cone search
    run_metrics : boolean
        run the inter night association metrics : trajectory_df, traj_next_night and new_observations parameters should have the
        ssnamenr column.

    Returns
    -------
    trajectory_df : dataframe
        the recorded trajectory increased by the new associated observations
    traj_next_night : dataframe
        the remaining tracklets of the new nights that have not been associated.
    new_observations : dataframe
        the remaining observations that have not been associated
    inter_night_report : dictionary
        statistics about the trajectory_association process, contains the following entries :

                    list of updated trajectories

                    all nid report with the following entries for each reports :

                                current nid

                                trajectories to tracklets report

                                number of trajectories to tracklets duplicated associations

                                trajectories to new observations report

                                number of trajectories to new observations duplicated associations

                                metrics, no sense if run_metrics is set to False

    Examples
    --------
    >>> trajectory_df, traj_next_night, new_observations, report = trajectory_associations(ts.trajectory_df_sample, ts.traj_next_night_sample, ts.new_observations_sample, 2 * u.degree, 0.2, 0.5, 30)

    >>> TestCase().assertDictEqual(ts.expected_trajectory_first_report, report)

    >>> assert_frame_equal(trajectory_df.reset_index(drop=True), ts.trajectory_df_expected)

    >>> assert_frame_equal(traj_next_night.reset_index(drop=True), ts.traj_next_night_expected)

    >>> assert_frame_equal(new_observations.reset_index(drop=True), ts.new_observations_expected)

    >>> trajectory_df, traj_next_night, new_observations, report = trajectory_associations(pd.DataFrame(), pd.DataFrame(), ts.new_observations_sample, 2 * u.degree, 0.2, 0.5, 30)

    >>> expected_report = {'list of updated trajectories': [], 'all nid report': []}
    >>> TestCase().assertDictEqual(expected_report, report)

    >>> assert_frame_equal(trajectory_df, pd.DataFrame())

    >>> assert_frame_equal(traj_next_night, pd.DataFrame())

    >>> assert_frame_equal(new_observations, ts.new_observations_sample)

    >>> trajectory_df, traj_next_night, new_observations, report = trajectory_associations(ts.trajectory_df_sample, pd.DataFrame(), ts.new_observations_sample, 2 * u.degree, 0.2, 0.5, 30)

    >>> TestCase().assertDictEqual(ts.expected_trajectory_second_report, report)

    >>> assert_frame_equal(trajectory_df.reset_index(drop=True), ts.trajectory_df_expected_empty)

    >>> assert_frame_equal(traj_next_night, pd.DataFrame())

    >>> assert_frame_equal(new_observations.reset_index(drop=True), ts.new_observations_expected)

    >>> trajectory_df, traj_next_night, new_observations, report = trajectory_associations(ts.trajectory_df_sample, ts.traj_next_night_sample, pd.DataFrame(), 2 * u.degree, 0.2, 0.5, 30)

    >>> TestCase().assertDictEqual(ts.expected_trajectory_third_report, report)

    >>> assert_frame_equal(trajectory_df.reset_index(drop=True), ts.trajectory_df_expected2)

    >>> assert_frame_equal(traj_next_night.reset_index(drop=True), ts.traj_next_night_expected)

    >>> assert_frame_equal(new_observations, pd.DataFrame())
    """

    trajectory_associations_report = dict()
    trajectory_associations_report["list of updated trajectories"] = []
    trajectory_associations_report["all nid report"] = []

    if len(trajectory_df) == 0:
        return (
            trajectory_df,
            traj_next_night,
            new_observations,
            trajectory_associations_report,
        )

    # if len(new_observations) > 0:
    #     next_nid = new_observations["nid"].values[0]
    # else:
    #     next_nid = traj_next_night["nid"].values[0]

    # if len(traj_next_night) > 0:
    #     # get the oldest extremity of the new tracklets to perform associations with the latest observations in the trajectories
    #     tracklets_extremity = get_n_last_observations_from_trajectories(
    #         traj_next_night, 1, False
    #     )
    # else:
    #     tracklets_extremity = pd.DataFrame(
    #         columns=["ra", "dec", "trajectory_id", "jd", "candid", "fid", "dcmag"]
    #     )

    all_nid_assoc_report = []

    trajectory_associations_report["all nid report"] = all_nid_assoc_report

    return (
        trajectory_df,
        traj_next_night,
        new_observations,
        trajectory_associations_report,
    )


def tracklets_and_observations_associations(
    trajectory_df,
    traj_next_night,
    old_observations,
    new_observations,
    last_trajectory_id,
    sep_criterion,
    mag_criterion_same_fid,
    mag_criterion_diff_fid,
    angle_criterion,
    run_metrics=False,
):
    """
    Perform the association process between the tracklets from the next night with the old observations.
    After that, associates the remaining old observations with the remaining new observations

    Parameters
    ----------
    trajectory_df : dataframe
        the recorded trajectory generate by the linkage algorithm
    traj_next_night : dataframe
        the tracklets from the new night
    old_observations : dataframe
        all the old observations that will not be associated before. The oldest observations are bounded by a time parameters.
    new_observations : dataframe
        new observations from the new night. not included in traj_next_night
    last_trajectory_id : integer
        the last trajectory id assign to a trajectory
    sep_criterion : float
        the separation criterion to associates alerts
    mag_criterion_same_fid : float
        the magnitude criterion to associates alerts if the observations have been observed with the same filter
    mag_criterion_diff_fid : float
        the magnitude criterion to associates alerts if the observations have been observed with the same filter
    angle_criterion : float
        the angle criterion to associates alerts during the cone search
    run_metrics : boolean
        run the inter night association metrics : trajectory_df, traj_next_night, old_observations and new_observations
        parameters should have the ssnamenr column.

    Returns
    -------
    trajectory_df : dataframe
        the recorded trajectory increased by the new associated observations
    old_observation : dataframe
        the new set of old observations with the not associated new observations
    inter_night_report : dictionary
        statistics about the tracklet and observation association process, contains the following entries :

                    list of updated trajectories

                    all nid report with the following entries for each of them :

                            current nid

                            old observation to tracklets report

                            number of tracklets to old observation duplicated association

                            old observation to new observation report

                            metrics, no sense if run_metrics is set to False

                    list of updated trajectories

    Examples
    --------
    >>> trajectory_df, old_observations, report = tracklets_and_observations_associations(
    ... ts.track_and_obs_trajectory_df_sample,
    ... ts.track_and_obs_traj_next_night_sample,
    ... ts.track_and_obs_old_observations_sample,
    ... ts.track_and_obs_new_observations_sample,
    ... 6,
    ... 1.5 * u.degree,
    ... 0.2,
    ... 0.5,
    ... 30
    ... )

    >>> TestCase().assertDictEqual(ts.expected_traj_obs_report, report)

    >>> assert_frame_equal(trajectory_df.reset_index(drop=True), ts.track_and_obs_trajectory_df_expected)

    >>> assert_frame_equal(old_observations.reset_index(drop=True), ts.track_and_obs_old_observations_expected)

    >>> trajectory_df, old_observations, report = tracklets_and_observations_associations(
    ... ts.track_and_obs_trajectory_df_sample,
    ... pd.DataFrame(),
    ... ts.track_and_obs_old_observations_sample,
    ... ts.track_and_obs_new_observations_sample,
    ... 6,
    ... 1.5 * u.degree,
    ... 0.2,
    ... 0.5,
    ... 30
    ... )

    >>> TestCase().assertDictEqual(ts.expected_traj_obs_report2, report)

    >>> assert_frame_equal(trajectory_df.reset_index(drop=True), ts.track_and_obs_trajectory_df_expected2, check_dtype=False)

    >>> assert_frame_equal(old_observations.reset_index(drop=True), ts.track_and_obs_old_observations_expected2, check_dtype=False)

    >>> trajectory_df, old_observations, report = tracklets_and_observations_associations(
    ... pd.DataFrame(),
    ... ts.track_and_obs_traj_next_night_sample,
    ... ts.track_and_obs_old_observations_sample,
    ... ts.track_and_obs_new_observations_sample,
    ... 6,
    ... 1.5 * u.degree,
    ... 0.2,
    ... 0.5,
    ... 30
    ... )

    >>> TestCase().assertDictEqual(ts.expected_traj_obs_report3, report)

    >>> assert_frame_equal(trajectory_df.reset_index(drop=True), ts.track_and_obs_trajectory_df_expected3)

    >>> assert_frame_equal(old_observations.reset_index(drop=True), ts.track_and_obs_old_observations_expected)

    >>> trajectory_df, old_observations, report = tracklets_and_observations_associations(
    ... ts.track_and_obs_trajectory_df_sample,
    ... ts.track_and_obs_traj_next_night_sample,
    ... pd.DataFrame(),
    ... ts.track_and_obs_new_observations_sample,
    ... 6,
    ... 1.5 * u.degree,
    ... 0.2,
    ... 0.5,
    ... 30
    ... )

    >>> expected_report = {'list of updated trajectories': [], 'all nid report': []}
    >>> TestCase().assertDictEqual(expected_report, report)

    >>> assert_frame_equal(trajectory_df.reset_index(drop=True), ts.track_and_obs_trajectory_df_expected4)

    >>> assert_frame_equal(old_observations.reset_index(drop=True), ts.track_and_obs_old_observations_expected3)

    >>> trajectory_df, old_observations, report = tracklets_and_observations_associations(
    ... ts.track_and_obs_trajectory_df_sample,
    ... ts.track_and_obs_traj_next_night_sample,
    ... ts.track_and_obs_old_observations_sample,
    ... pd.DataFrame(),
    ... 6,
    ... 1.5 * u.degree,
    ... 0.2,
    ... 0.5,
    ... 30
    ... )

    >>> TestCase().assertDictEqual(ts.expected_traj_obs_report4, report)

    >>> assert_frame_equal(trajectory_df.reset_index(drop=True), ts.track_and_obs_trajectory_df_expected5)

    >>> assert_frame_equal(old_observations.reset_index(drop=True), ts.track_and_obs_old_observations_expected4)

    >>> trajectory_df, old_observations, report = tracklets_and_observations_associations(
    ... ts.track_and_obs_trajectory_df_sample,
    ... pd.DataFrame(),
    ... pd.DataFrame(),
    ... ts.track_and_obs_new_observations_sample,
    ... 6,
    ... 1.5 * u.degree,
    ... 0.2,
    ... 0.5,
    ... 30
    ... )

    >>> expected_report = {'list of updated trajectories': [], 'all nid report': []}
    >>> TestCase().assertDictEqual(expected_report, report)

    >>> assert_frame_equal(trajectory_df.reset_index(drop=True), ts.track_and_obs_trajectory_df_sample)

    >>> assert_frame_equal(old_observations.reset_index(drop=True), ts.track_and_obs_new_observations_sample)

    >>> trajectory_df, old_observations, report = tracklets_and_observations_associations(
    ... ts.track_and_obs_trajectory_df_sample,
    ... pd.DataFrame(),
    ... ts.track_and_obs_old_observations_sample,
    ... pd.DataFrame(),
    ... 6,
    ... 1.5 * u.degree,
    ... 0.2,
    ... 0.5,
    ... 30
    ... )

    >>> expected_report = {'list of updated trajectories': [], 'all nid report': []}
    >>> TestCase().assertDictEqual(expected_report, report)

    >>> assert_frame_equal(trajectory_df.reset_index(drop=True), ts.track_and_obs_trajectory_df_sample)

    >>> assert_frame_equal(old_observations.reset_index(drop=True), ts.track_and_obs_old_observations_sample)
    """

    track_and_obs_report = dict()
    track_and_obs_report["list of updated trajectories"] = []
    track_and_obs_report["all nid report"] = []

    if len(old_observations) == 0:
        if len(traj_next_night) > 0:
            return (
                pd.concat([trajectory_df, traj_next_night]),
                new_observations,
                track_and_obs_report,
            )
        else:
            return trajectory_df, new_observations, track_and_obs_report

    if len(new_observations) > 0:
        next_nid = new_observations["nid"].values[0]
    elif len(traj_next_night) > 0:
        next_nid = traj_next_night["nid"].values[0]
    else:
        return trajectory_df, old_observations, track_and_obs_report

    old_obs_nid = np.sort(np.unique(old_observations["nid"]))[::-1]

    traj_next_night = pd.DataFrame(
        columns=["ra", "dec", "trajectory_id", "jd", "candid", "fid", "dcmag"]
    )
    two_first_obs_tracklets = pd.DataFrame(
        columns=["ra", "dec", "trajectory_id", "jd", "candid", "fid", "dcmag"]
    )

    all_nid_report = []

    for obs_nid in old_obs_nid:

        current_nid_report = dict()

        current_old_obs = old_observations[old_observations["nid"] == obs_nid]

        current_nid_report["old nid"] = int(obs_nid)

        diff_night = next_nid - obs_nid
        norm_sep_crit = sep_criterion * diff_night
        norm_same_fid = mag_criterion_same_fid * diff_night
        norm_diff_fid = mag_criterion_diff_fid * diff_night

        # association between the new tracklets and the old observations
        (
            traj_left,
            old_obs_right,
            track_to_old_obs_report,
        ) = night_to_night_trajectory_associations(
            two_first_obs_tracklets,
            current_old_obs,
            norm_sep_crit,
            norm_same_fid,
            norm_diff_fid,
            angle_criterion,
        )

        nb_track_to_obs_assoc_with_duplicates = len(old_obs_right)
        track_to_old_obs_report["number of duplicated association"] = 0
        track_to_old_obs_report["metrics"] = {}

        if len(traj_left) > 0:

            # remove the duplicates()
            old_obs_right = old_obs_right.drop_duplicates(["trajectory_id"])
            traj_left = traj_left.drop_duplicates(["trajectory_id"])

            track_to_old_obs_report[
                "number of duplicated association"
            ] = nb_track_to_obs_assoc_with_duplicates - len(old_obs_right)

            traj_next_night = pd.concat([traj_next_night, old_obs_right])

            two_first_obs_tracklets = two_first_obs_tracklets[
                ~two_first_obs_tracklets["trajectory_id"].isin(
                    traj_left["trajectory_id"]
                )
            ]

            old_observations = old_observations[
                ~old_observations["candid"].isin(old_obs_right["candid"])
            ]
            current_old_obs = current_old_obs[
                ~current_old_obs["candid"].isin(old_obs_right["candid"])
            ]

        if run_metrics:
            last_traj_obs = (
                two_first_obs_tracklets.groupby(["trajectory_id"]).last().reset_index()
            )
            inter_night_metric = compute_inter_night_metric(
                last_traj_obs, current_old_obs, traj_left, old_obs_right
            )
            track_to_old_obs_report["metrics"] = inter_night_metric

        current_nid_report[
            "old observation to tracklets report"
        ] = track_to_old_obs_report

        current_nid_report["old observation to new observation report"] = {
            "number of inter night separation based association": 0,
            "number of inter night magnitude filtered association": 0,
            "number of inter night angle filtered association": 0,
            "number of duplicated association": 0,
            "metrics": {},
        }

        if len(new_observations) > 0:

            (
                left_assoc,
                right_assoc,
                old_to_new_assoc_report,
            ) = night_to_night_observation_association(
                current_old_obs,
                new_observations,
                norm_sep_crit,
                norm_same_fid,
                norm_diff_fid,
            )

            if run_metrics:
                inter_night_metric = compute_inter_night_metric(
                    current_old_obs, new_observations, left_assoc, right_assoc
                )
                old_to_new_assoc_report["metrics"] = inter_night_metric

            old_to_new_assoc_report["number of duplicated association"] = 0
            old_to_new_assoc_report[
                "number of inter night angle filtered association"
            ] = 0

            if len(left_assoc) > 0:

                new_trajectory_id = np.arange(
                    last_trajectory_id, last_trajectory_id + len(left_assoc)
                )

                last_trajectory_id = last_trajectory_id + len(left_assoc)

                # remove the associated old observation
                old_observations = old_observations[
                    ~old_observations["candid"].isin(left_assoc["candid"])
                ]

                # remove the associated new observation
                new_observations = new_observations[
                    ~new_observations["candid"].isin(right_assoc["candid"])
                ]

                # assign a new trajectory id to the new association
                left_assoc["trajectory_id"] = right_assoc[
                    "trajectory_id"
                ] = new_trajectory_id

                trajectory_df = pd.concat([trajectory_df, left_assoc, right_assoc])

                track_and_obs_report["list of updated trajectories"] = np.union1d(
                    track_and_obs_report["list of updated trajectories"],
                    np.unique(left_assoc["trajectory_id"]),
                ).tolist()

            current_nid_report[
                "old observation to new observation report"
            ] = old_to_new_assoc_report

        all_nid_report.append(current_nid_report)

    track_and_obs_report["all nid report"] = all_nid_report
    track_and_obs_report["list of updated trajectories"] = np.union1d(
        track_and_obs_report["list of updated trajectories"],
        np.unique(traj_next_night["trajectory_id"]),
    ).tolist()

    trajectory_df = pd.concat([trajectory_df, traj_next_night])

    return (
        trajectory_df,
        pd.concat([old_observations, new_observations]),
        track_and_obs_report,
    )


def time_window_management(
    trajectory_df, old_observation, last_nid, nid_next_night, time_window
):
    """
    Management of the old observation and trajectories. Remove the old observation with a nid difference with
    the nid of the next night greater than the time window. Perform the same process for trajectories but take
    the most recent trajectory extremity.

    Remove also the trajectories with no computed orbit element.

    If a number of night without observation exceeds the time window parameters, keep the observations and trajectories
    from the night before the non observation gap.

    Parameters
    ----------
    trajectory_df : dataframe
        all recorded trajectories
    old_observation : dataframe
        old observation from previous night
    last_nid : integer
        nid of the previous observation night
    nid_next_night : integer
        nid of the incoming night
    time_window : integer
        limit to keep old observation and trajectories

    Return
    ------
    oldest_traj : dataframe
        the trajectories older than the time window
    most_recent_traj : dataframe
        the trajectories with an nid from an extremity observation smaller than the time window
    old_observation : dataframe
        all the old observation with a difference of nid with the next incoming nid smaller than
        the time window

    Examples
    --------
    >>> test_traj = pd.DataFrame({
    ... "candid" : [10, 11, 12, 13, 14, 15],
    ... "nid" : [1, 2, 3, 10, 11, 12],
    ... "jd" : [1, 2, 3, 10, 11, 12],
    ... "trajectory_id" : [1, 1, 1, 2, 2, 2]
    ... })

    >>> test_obs = pd.DataFrame({
    ... "nid" : [1, 4, 11, 12],
    ... "candid" : [16, 17, 18, 19]
    ... })

    >>> (test_old_traj, test_most_recent_traj), test_old_obs = time_window_management(test_traj, test_obs, 12, 17, 3)

    >>> expected_old_traj = pd.DataFrame({
    ... "candid" : [10, 11, 12],
    ... "nid" : [1, 2, 3],
    ... "jd" : [1, 2, 3],
    ... "trajectory_id" : [1, 1, 1]
    ... })

    >>> expected_most_recent_traj = pd.DataFrame({
    ... "candid" : [13, 14, 15],
    ... "nid" : [10, 11, 12],
    ... "jd" : [10, 11, 12],
    ... "trajectory_id" : [2, 2, 2]
    ... })

    >>> expected_old_obs = pd.DataFrame({
    ... "nid" : [12],
    ... "candid" : [19]
    ... })

    >>> assert_frame_equal(expected_old_traj.reset_index(drop=True), test_old_traj.reset_index(drop=True))
    >>> assert_frame_equal(expected_most_recent_traj.reset_index(drop=True), test_most_recent_traj.reset_index(drop=True))
    >>> assert_frame_equal(expected_old_obs.reset_index(drop=True), test_old_obs.reset_index(drop=True))
    """
    most_recent_traj = pd.DataFrame()
    oldest_traj = pd.DataFrame()

    if len(trajectory_df) > 0:

        # get the lost observation of all trajectories
        last_obs_of_all_traj = get_n_last_observations_from_trajectories(
            trajectory_df, 1
        )

        # if the night difference exceed the time window
        if nid_next_night - last_nid > time_window:

            # get last observation of trajectories from the last nid
            last_obs_of_all_traj = last_obs_of_all_traj[
                last_obs_of_all_traj["nid"] == last_nid
            ]

            mask_traj = trajectory_df["trajectory_id"].isin(
                last_obs_of_all_traj["trajectory_id"]
            )
            most_recent_traj = trajectory_df[mask_traj]
            oldest_traj = trajectory_df[~mask_traj & (trajectory_df["a"] != -1.0)]
            old_observation = old_observation[old_observation["nid"] == last_nid]

            # return the trajectories from the last night id
            return (oldest_traj, most_recent_traj), old_observation

        last_obs_of_all_traj["diff_nid"] = nid_next_night - last_obs_of_all_traj["nid"]

        most_recent_last_obs = last_obs_of_all_traj[
            last_obs_of_all_traj["diff_nid"] <= time_window
        ]

        mask_traj = trajectory_df["trajectory_id"].isin(
            most_recent_last_obs["trajectory_id"]
        )

        most_recent_traj = trajectory_df[mask_traj]
        oldest_traj = trajectory_df[~mask_traj & (trajectory_df["a"] != -1.0)]

    diff_nid_old_observation = nid_next_night - old_observation["nid"]
    old_observation = old_observation[diff_nid_old_observation < time_window]

    return (oldest_traj, most_recent_traj), old_observation


if __name__ == "__main__":  # pragma: no cover
    import sys
    import doctest
    from pandas.testing import assert_frame_equal  # noqa: F401
    import test_sample as ts  # noqa: F401
    from unittest import TestCase  # noqa: F401

    if "unittest.util" in __import__("sys").modules:
        # Show full diff in self.assertEqual.
        __import__("sys").modules["unittest.util"]._MAX_LENGTH = 999999999

    sys.exit(doctest.testmod()[0])
