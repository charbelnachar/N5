import api from '../api';
import { ADD_INFRACTION, GET_INFRACTIONS, UPDATE_INFRACTION, DELETE_INFRACTION } from './types';

export const addInfraction = (infraction) => async dispatch => {
  try {
    const response = await api.post('/cargar_infraccion/', infraction);
    dispatch({ type: ADD_INFRACTION, payload: response.data });
  } catch (error) {
    console.error(error);
  }
};

export const getInfractions = () => async dispatch => {
  try {
    const response = await api.get('/get_all_infraccion/');
    dispatch({ type: GET_INFRACTIONS, payload: response.data });
  } catch (error) {
    console.error(error);
  }
};

export const updateInfraction = (id, infraction) => async dispatch => {
  try {
    const response = await api.put(`/infraccion/${id}/`, infraction);
    dispatch({ type: UPDATE_INFRACTION, payload: response.data });
  } catch (error) {
    console.error(error);
  }
};

export const deleteInfraction = (id) => async dispatch => {
  try {
    await api.delete(`/infraccion/${id}/`);
    dispatch({ type: DELETE_INFRACTION, payload: id });
  } catch (error) {
    console.error(error);
  }
};
