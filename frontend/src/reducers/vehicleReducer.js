import { ADD_VEHICLE, GET_VEHICLES, UPDATE_VEHICLE, DELETE_VEHICLE } from '../actions/types';

const initialState = {
  vehicles: [],
};

export default function vehicleReducer(state = initialState, action) {
  switch (action.type) {
    case ADD_VEHICLE:
      return {
        ...state,
        vehicles: state.vehicles.map(vehicle =>
          vehicle.license_plate === action.payload.license_plate ? action.payload : vehicle),
      };
    case GET_VEHICLES:
      return {
        ...state,
        vehicles: action.payload,
      };
    case UPDATE_VEHICLE:
      return {
        ...state,
        vehicles: state.vehicles.map(vehicle =>
          vehicle.license_plate === action.payload.license_plate ? action.payload : vehicle
        ),
      };
    case DELETE_VEHICLE:
      return {
        ...state,
        vehicles: state.vehicles.filter(vehicle => vehicle.license_plate !== action.payload),
      };
    default:
      return state;
  }
}
