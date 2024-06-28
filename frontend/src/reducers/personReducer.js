// src/reducers/personReducer.js
import { ADD_PERSON, GET_ALL_PERSONS,API_ERROR } from '../actions/types';

const initialState = {
  persons: [],error: '',
};

export default function (state = initialState, action) {
  switch (action.type) {
    case API_ERROR:
      return {
        ...state,
        error: action.payload
      };
    case ADD_PERSON:
      return {
        ...state,
        persons: [...state.persons, action.payload],
        error: '',
      };
    case GET_ALL_PERSONS:
      return {
        ...state,
        persons: action.payload,
        
      };
    default:
      return state;
  }
}
