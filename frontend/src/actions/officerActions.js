import api from '../api';
import { ADD_OFFICER, GET_OFFICERS, UPDATE_OFFICER, DELETE_OFFICER, CLEAR_OFFICER_DATA, SET_OFFICER_ERROR, CLEAR_OFFICER_ERROR } from './types';

export const addOfficer = (officer) => async dispatch => {
  try {
    const response = await api.post('/officer/', officer);
    dispatch({ type: ADD_OFFICER, payload: response.data });
    dispatch({ type: CLEAR_OFFICER_ERROR });
  } catch (error) {
    const errorMessage = error.response?.data?.error || 'An error occurred while adding officer';
    console.log(errorMessage);
    dispatch({ type: SET_OFFICER_ERROR, payload: errorMessage });
  }
};

export const getOfficers = () => async dispatch => {
  try {
    const response = await api.get('/all_officer/');
    console.log(response.data.data);
    dispatch({ type: GET_OFFICERS, payload: response.data.data });
  } catch (error) {
    const errorMessage = error.response?.data?.error || 'An error occurred while fetching officers';
    console.error(errorMessage);
    dispatch({ type: SET_OFFICER_ERROR, payload: errorMessage });
  }
};

export const updateOfficer = (username, officer) => async dispatch => {
  try {
    console.log(officer);
    const response = await api.put(`/officer/${officer['identifier']}/`, officer);
    dispatch({ type: UPDATE_OFFICER, payload: response.data });
    dispatch({ type: CLEAR_OFFICER_DATA });
    dispatch({ type: CLEAR_OFFICER_ERROR });
  } catch (error) {
    const errorMessage = error.response?.data?.error || 'An error occurred while updating officer';
    console.error(errorMessage);
    dispatch({ type: SET_OFFICER_ERROR, payload: errorMessage });
  }
};

export const deleteOfficer = (username) => async dispatch => {
  try {
    await api.delete(`/officer/${username}/`);
    dispatch({ type: DELETE_OFFICER, payload: username });
    dispatch({ type: CLEAR_OFFICER_DATA });
    dispatch({ type: CLEAR_OFFICER_ERROR });
  } catch (error) {
    const errorMessage = error.response?.data?.error || 'An error occurred while deleting officer';
    console.error(errorMessage);
    dispatch({ type: SET_OFFICER_ERROR, payload: errorMessage });
  }
};
