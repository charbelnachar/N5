import api from '../api';
import { ADD_PERSON, GET_ALL_PERSONS, UPDATE_PERSON, DELETE_PERSON,API_ERROR } from './types';

export const addPerson = (person) => async dispatch => {
  try {
    
    const response = await api.post('/person/', person);
    dispatch({ type: ADD_PERSON, payload: response.data });
    dispatch({ type: API_ERROR, payload: "" });
  } catch (error) {
    dispatch({ type: API_ERROR, payload: error.response.data.error });
  }
};

export const getAllPersons = () => async dispatch => {
  try {
    const response = await api.get('/all_person');
    dispatch({ type: GET_ALL_PERSONS, payload: response.data.data });
  } catch (error) {
 

  }
};

export const updatePerson = (id, person) => async dispatch => {
  try {
    console.log(id);
    const response = await api.put(`/person/${id}/`, person);
    dispatch({ type: UPDATE_PERSON, payload: response.data });
    dispatch({ type: API_ERROR, payload: "" });
  } catch (error) {

    dispatch({ type: API_ERROR, payload: error.response.data.error });
  }
};

export const deletePerson = (id) => async dispatch => {
  try {
    await api.delete(`/person/${id}/`);
    dispatch({ type: DELETE_PERSON, payload: id });
    dispatch({ type: API_ERROR, payload: "" });
  } catch (error) {
    console.error(error);
    dispatch({ type: API_ERROR, payload: error.response.data });
  }
};
