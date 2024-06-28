// src/components/PersonForm.js
import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { addPerson } from '../actions/personActions';
import styled from 'styled-components';
import { useSelector } from 'react-redux';


const FormContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
`;

const Form = styled.form`
  display: flex;
  flex-direction: column;
  align-items: center;
`;

const FormField = styled.div`
  margin-bottom: 10px;
`;

const PersonForm = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const error = useSelector(state => state.persons.error);
  const dispatch = useDispatch();

  const handleSubmit = (e) => {
    e.preventDefault();
    const person = { name, email };
    dispatch(addPerson(person));
  };

  return (
    <FormContainer>
      <h2>Cargar Persona</h2>
      <Form onSubmit={handleSubmit}>
        <FormField>
          <label>Nombre:</label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
        </FormField>
        <FormField>
          <label>Email:</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </FormField>
        <button type="submit">Submit</button>
      </Form>
    </FormContainer>
  );
};

export default PersonForm;
