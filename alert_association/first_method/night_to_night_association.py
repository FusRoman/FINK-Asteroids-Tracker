from astropy.coordinates.solar_system import get_body_barycentric
import astropy.units as u
from astropy.coordinates import SkyCoord
import pandas as pd
import numpy as np
from collections import Counter
import time as t

from pandas.core.indexes import multi

from intra_night_association import intra_night_association
from intra_night_association import new_trajectory_id_assignation
from intra_night_association import magnitude_association
from intra_night_association import removed_mirrored_association



def night_to_night_separation_association(old_observation, new_observation, separation_criterion):
    """
    Perform night-night association based on the separation between the alerts. The separation criterion was computed by a data analysis on the MPC object.

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
    """

    old_observations_coord = SkyCoord(old_observation['ra'], old_observation['dec'], unit=u.degree)
    new_observations_coord = SkyCoord(new_observation['ra'], new_observation['dec'], unit=u.degree)

    
    # 108.07 arcsecond come from our study of the intra-night separation between the alerts from the same nights. 52 take 99 percents of the objects.
    new_obs_idx, old_obs_idx, sep2d, _ = old_observations_coord.search_around_sky(new_observations_coord, separation_criterion)

    old_obs_assoc = old_observation.iloc[old_obs_idx]
    new_obs_assoc = new_observation.iloc[new_obs_idx]
    return old_obs_assoc, new_obs_assoc, sep2d


def get_last_observations_from_trajectories(trajectories):
    sort_jd = trajectories.sort_values(['jd'])

    last_occurence = sort_jd.drop_duplicates(['trajectory_id'], keep='last')

    return last_occurence


def night_to_night_association(trajectory_df, old_observation, new_observation, sep_criterion=0.43*u.degree, mag_criterion_same_fid=1.36, mag_criterion_diff_fid=1.31):

    last_observation_trajectory = get_last_observations_from_trajectories(trajectory_df)

    last_trajectory_id = np.max(last_observation_trajectory['trajectory_id'].values) + 1

    # trajectory association with the new tracklets

    # intra-night association of the new observations
    new_left, new_right, _ = intra_night_association(new_observation)

    # night_to_night association between the last observations from the trajectories and the new observations of the next night
    traj_assoc, new_obs_assoc, _ = night_to_night_separation_association(last_observation_trajectory, new_left, sep_criterion)
    traj_assoc, new_obs_assoc = magnitude_association(traj_assoc, new_obs_assoc, mag_criterion_same_fid, mag_criterion_diff_fid)
    traj_assoc, new_obs_assoc = removed_mirrored_association(traj_assoc, new_obs_assoc)

    

    traj_assoc = traj_assoc.reset_index(drop=True).reset_index()
    new_obs_assoc = new_obs_assoc.reset_index(drop=True)

    #print(traj_assoc)

    new_obs_assoc['trajectory_id'] = traj_assoc['trajectory_id']

    # get alerts with multiple associations
    gb_traj = traj_assoc.groupby(['candid']).agg(
        {
            "index" : list,
            "candid" : list,
            "ra" : lambda x : len(x)
        }
    )

    #print(gb_traj)

    multiple_assoc = gb_traj[gb_traj['ra'] > 1]

    if len(gb_traj) > 0:
        print("multiple assoc prop : {}".format(np.sum(multiple_assoc['ra']) / np.sum(gb_traj['ra']) * 100))
    else:
        print("nb assoc : {}".format(len(gb_traj)))

    return None, None

    all_multiple_candid = multiple_assoc.explode(['index', 'candid'])

    # create new trajectory index for the duplicates
    new_traj_id = np.arange(last_trajectory_id, last_trajectory_id + len(all_multiple_candid))

    # set candid column as new index to recover the right rows.
    traj_assoc.set_index(['candid'], inplace=True)

    # set a new trajectory id to all multiple associations
    # use candid index for traj_assoc 
    # becarefull, np.unique in the all_multiple_candid is required because loc get rows for each instance of candid so that creates duplicates on the results
    traj_assoc.loc[np.unique(all_multiple_candid['candid'].values), 'tmp_traj_id'] = new_traj_id
    new_obs_assoc.loc[np.unique(all_multiple_candid['index'].values), 'tmp_traj_id'] = new_traj_id
    traj_assoc = traj_assoc.reset_index()
    new_obs_assoc = new_obs_assoc.reset_index()

    # aggregate the new trajectory_id with the first trajectory_id
    gb_traj = traj_assoc.groupby(['trajectory_id']).agg(
        traj_size=("candid", lambda x : len(x)),
        tmp_traj=('tmp_traj_id', list)
    )

    gb_traj = gb_traj[gb_traj['traj_size'] > 1]

    # the first multiple associations take the original trajecotry_id 
    agg_traj_id = gb_traj['tmp_traj'].values
    for traj_id, new_traj_idx in zip(gb_traj.index.values, range(len(agg_traj_id))):
        agg_traj_id[new_traj_idx][0] = traj_id


    gb_traj['tmp_traj'] = agg_traj_id

    trajectory_df = trajectory_df.set_index(['trajectory_id'])
    trajectory_df.loc[trajectory_df.index.values, 'trajectory_id'] = gb_traj['tmp_traj']

    print(trajectory_df.loc[171])



    #print(np.unique(pd.concat([last_observation_trajectory, new_obs_assoc]).groupby(['trajectory_id']).count()['ra']))

    return None, None

    track_assoc_left_columns = [el + "_x" for el in list(new_obs_assoc.columns)[:-2]] + ['trajectory_id']
    track_assoc_right_columns = [el + "_y" for el in list(new_obs_assoc.columns)[:-2]]

    track_assoc = new_obs_assoc.merge(new_right, on='tmp_traj_id')

    

    left_tracklets = track_assoc[track_assoc_left_columns]
    right_tracklets = track_assoc[track_assoc_right_columns]
    right_tracklets['trajectory_id'] = left_tracklets['trajectory_id']
    

    left_new_name = {k:v  for v, k in zip(list(new_obs_assoc.columns)[:-2], track_assoc_left_columns)}
    right_new_name = {k:v  for v, k in zip(list(new_obs_assoc.columns)[:-2], track_assoc_right_columns)}
    
    left_tracklets = left_tracklets.rename(left_new_name, axis=1)
    right_tracklets = right_tracklets.rename(right_new_name, axis=1)

    return None, None

    # trajectory association with new_observation
    traj_assoc, new_traj_obs, _ = night_to_night_separation_association(last_observation_trajectory, new_observation, sep_criterion)
    traj_assoc, new_traj_obs = magnitude_association(traj_assoc, new_traj_obs, mag_criterion_same_fid, mag_criterion_diff_fid)

    traj_assoc = traj_assoc.reset_index(drop=True)
    new_traj_obs = new_traj_obs.reset_index(drop=True)

    new_traj_obs['trajectory_id'] = traj_assoc['trajectory_id']
    new_observation = new_observation[~new_observation['candid'].isin(new_traj_obs['candid'])]

    old_obs_assoc, new_obs_assoc, _ = night_to_night_separation_association(old_observation, new_observation, sep_criterion)

    #old_assoc, new_assoc = intra_night_magnitude_association(old_obs_assoc, new_obs_assoc, mag_criterion_same_fid, mag_criterion_diff_fid)

    return traj_assoc, new_traj_obs



if __name__ == "__main__":
    df_sso = pd.read_pickle("../../data/month=03")

    df_sso = df_sso.drop_duplicates(['candid'])

    all_night = np.unique(df_sso['nid'])
    print(all_night)

    for i in range(len(all_night)-1):
        t_before = t.time()
        n1 = all_night[i]
        n2 = all_night[i+1]
        if n2 - n1 == 1:
            print(n1)
            print(n2)
            print()
            df_night1 = df_sso[(df_sso['nid'] == n1) & (df_sso['fink_class'] == 'Solar System MPC')]
            df_night2 = df_sso[(df_sso['nid'] == n2) & (df_sso['fink_class'] == 'Solar System MPC')]

            left, right, _ = intra_night_association(df_night1)
            traj_df = new_trajectory_id_assignation(left, right, 0)
            traj_df = traj_df.reset_index(drop=True)

            old_observation = df_night1[~df_night1['candid'].isin(traj_df['candid'])]

            old_assoc, new_assoc = night_to_night_association(traj_df, old_observation, df_night2)
        print("elapsed time: {}".format(t.time() - t_before))