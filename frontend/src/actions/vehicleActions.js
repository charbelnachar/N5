import api from '../api';
import { ADD_VEHICLE, GET_VEHICLES, UPDATE_VEHICLE,API_ERROR, DELETE_VEHICLE } from './types';

export const addVehicle = (vehicle) => async dispatch => {
  try {
    
    const response = await api.post('/vehicle/', vehicle);
    console.log(response);
    dispatch({ type: ADD_VEHICLE, payload: response.data });
  } catch (error) {
    dispatch({ type:API_ERROR , payload: error.response.data.error });
    console.error(error);
  }
};

export const getVehicles = () => async dispatch => {
  try {
    const response = await api.get('/get_all_vehicles/');
    dispatch({ type: GET_VEHICLES, payload: response.data.data });
  } catch (error) {
    console.error(error);
  }
};

export const updateVehicle = (licensePlate, vehicle) => async dispatch => {
  try {
    const response = await api.put(`/vehicle/${licensePlate}/`, vehicle);
    dispatch({ type: UPDATE_VEHICLE, payload: response.data });
  } catch (error) {
    dispatch({ type:API_ERROR , payload: error.response.data.error });
    console.error(error);
  }
};

export const deleteVehicle = (licensePlate) => async dispatch => {
  try {
    await api.delete(`/vehicle/${licensePlate}/`);
    dispatch({ type: DELETE_VEHICLE, payload: licensePlate });
  } catch (error) {
    dispatch({ type:API_ERROR , payload: error.response.data.error });
    console.error(error);
  }
};
