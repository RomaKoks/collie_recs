import os

import numpy as np
import pandas as pd
import pytest

from collie_recs.utils import create_ratings_matrix, pandas_df_to_hdf5


@pytest.fixture()
def df_for_interactions():
    # this should exactly match ``ratings_matrix_for_interactions`` below
    return pd.DataFrame(data={
        'user_id': [0, 0, 1, 1, 2, 2, 2, 3, 3, 3, 4, 5],
        'item_id': [1, 2, 2, 3, 4, 5, 6, 7, 8, 9, 0, 3],
        'rating': [1, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 5],
    })


@pytest.fixture()
def ratings_matrix_for_interactions():
    # this should exactly match ``df_for_interactions`` above
    return np.array([[0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 2, 3, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 4, 5, 1, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 2, 3, 4],
                     [5, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 5, 0, 0, 0, 0, 0, 0]])


@pytest.fixture()
def sparse_ratings_matrix_for_interactions(df_for_interactions):
    return create_ratings_matrix(df=df_for_interactions,
                                 user_col='user_id',
                                 item_col='item_id',
                                 ratings_col='rating',
                                 sparse=True)


@pytest.fixture()
def df_for_interactions_with_missing_ids():
    # we are missing item ID 7
    # this should exactly match ``ratings_matrix_for_interactions_with_missing_ids`` below
    return pd.DataFrame(data={
        'user_id': [0, 0, 1, 1, 2, 2, 2, 3, 3, 3, 4, 5],
        'item_id': [1, 2, 2, 3, 4, 5, 6, 0, 8, 9, 0, 3],
        'rating': [1, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 5],
    })


@pytest.fixture()
def ratings_matrix_for_interactions_with_missing_ids():
    # we are missing item ID 7
    # this should exactly match ``df_for_interactions_with_missing_ids`` above
    return np.array([[0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 2, 3, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 4, 5, 1, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [5, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 5, 0, 0, 0, 0, 0, 0]])


@pytest.fixture()
def sparse_ratings_matrix_for_interactions_with_missing_ids(df_for_interactions_with_missing_ids):
    return create_ratings_matrix(df=df_for_interactions_with_missing_ids,
                                 user_col='user_id',
                                 item_col='item_id',
                                 ratings_col='rating',
                                 sparse=True)


@pytest.fixture()
def hdf5_pandas_df_path(df_for_interactions, tmpdir):
    hdf5_path = os.path.join(str(tmpdir), 'df_for_interactions.h5')
    pandas_df_to_hdf5(df=df_for_interactions, out_path=hdf5_path, key='interactions')

    return hdf5_path


@pytest.fixture()
def hdf5_pandas_df_path_with_meta(df_for_interactions, tmpdir):
    hdf5_path = os.path.join(str(tmpdir), 'df_for_interactions_meta.h5')
    pandas_df_to_hdf5(df=df_for_interactions, out_path=hdf5_path, key='interactions')

    additional_info_df = pd.DataFrame({
        'num_users': [df_for_interactions['user_id'].max() + 1],
        'num_items': [df_for_interactions['item_id'].max() + 1],
    })
    pandas_df_to_hdf5(df=additional_info_df, out_path=hdf5_path, key='meta')

    return hdf5_path


@pytest.fixture(params=['users', 'items', 'both_users_and_items'])
def hdf5_pandas_df_path_ids_start_at_1(request, df_for_interactions, tmpdir):
    incremented_df_for_interactions = df_for_interactions

    if 'users' in request.param:
        incremented_df_for_interactions['user_id'] += 1
    if 'items' in request.param:
        incremented_df_for_interactions['item_id'] += 1

    hdf5_path = os.path.join(str(tmpdir), 'df_for_interactions_incremented.h5')
    pandas_df_to_hdf5(df=incremented_df_for_interactions, out_path=hdf5_path, key='interactions')

    return hdf5_path
