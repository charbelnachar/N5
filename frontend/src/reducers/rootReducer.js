import { combineReducers } from 'redux';
import authReducer from './authReducer';
import infractionReducer from './infractionReducer';
import personReducer from './personReducer';
import vehicleReducer from './vehicleReducer';
import officerReducer from './officerReducer';

export default combineReducers({
  auth: authReducer,
  infractions: infractionReducer,
  persons: personReducer,
  vehicles: vehicleReducer,
  officers: officerReducer,
});
