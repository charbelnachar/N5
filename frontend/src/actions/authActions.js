import api from '../api';
import { LOGIN_SUCCESS, LOGIN_FAIL } from './types';

export const login = (username, password) => async dispatch => {
  try {
    const response = await api.post('/api/token/', { username, password });
    const { access } = response.data;
    localStorage.setItem('token', access);
    dispatch({ type: LOGIN_SUCCESS, payload: access });
    return true;
  } catch (error) {
    const errorMessage = error.response && error.response.data && error.response.data.detail
      ? error.response.data.detail
      : 'Login failed. Please try again.';
    dispatch({ type: LOGIN_FAIL, payload: errorMessage });
    return false;
  }
};

export const loginSuccess = (token) => dispatch => {
  dispatch({ type: LOGIN_SUCCESS, payload: token });
};
