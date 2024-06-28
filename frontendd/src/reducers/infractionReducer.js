import { ADD_INFRACTION, GET_INFRACTIONS, UPDATE_INFRACTION, DELETE_INFRACTION } from '../actions/types';

const initialState = {
  infractions: [],
};

export default function infractionReducer(state = initialState, action) {
  switch (action.type) {
    case ADD_INFRACTION:
      return {
        ...state,
        infractions: [...state.infractions, action.payload],
      };
    case GET_INFRACTIONS:
      return {
        ...state,
        infractions: action.payload,
      };
    case UPDATE_INFRACTION:
      return {
        ...state,
        infractions: state.infractions.map(infraction =>
          infraction.id === action.payload.id ? action.payload : infraction
        ),
      };
    case DELETE_INFRACTION:
      return {
        ...state,
        infractions: state.infractions.filter(infraction => infraction.id !== action.payload),
      };
    default:
      return state;
  }
}
