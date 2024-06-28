import { ADD_OFFICER, GET_OFFICERS, UPDATE_OFFICER, DELETE_OFFICER, CLEAR_OFFICER_DATA, SET_OFFICER_ERROR, CLEAR_OFFICER_ERROR } from '../actions/types';

const initialState = {
  officers: [],
  error: null,
};

export default function officerReducer(state = initialState, action) {
  switch (action.type) {
    case ADD_OFFICER:
      return {
        ...state,
        officers: [...state.officers, action.payload],
      };
    case GET_OFFICERS:
      return {
        ...state,
        officers: action.payload,
      };
    case UPDATE_OFFICER:
      return {
        ...state,
        officers: state.officers.map(officer =>
          officer.username === action.payload.username ? action.payload : officer
        ),
      };
    case DELETE_OFFICER:
      return {
        ...state,
        officers: state.officers.filter(officer => officer.username !== action.payload),
      };
    case SET_OFFICER_ERROR:
      return {
        ...state,
        error: action.payload,
      };
    case CLEAR_OFFICER_ERROR:
      return {
        ...state,
        error: null,
      };
    case CLEAR_OFFICER_DATA:
      return {
        ...state,
        inputs: {
          username: '',
          name: '',
          email: '',
          password: '',
          identifier: '',
        },
      };
    default:
      return state;
  }
}
