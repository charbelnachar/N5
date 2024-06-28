import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { addOfficer, getOfficers } from '../actions/officerActions';
import styled from 'styled-components';

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

const SuccessMessage = styled.div`
  color: green;
  margin-bottom: 10px;
`;

const OfficerForm = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [success, setSuccess] = useState('');
  const dispatch = useDispatch();
  const officers = useSelector(state => state.officers.officers);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const officer = { name, email };
    await dispatch(addOfficer(officer));
    setSuccess('Officer created successfully!');
    dispatch(getOfficers());
  };

  return (
    <FormContainer>
      <h2>Cargar Oficial</h2>
      {success && <SuccessMessage>{success}</SuccessMessage>}
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

export default OfficerForm;
