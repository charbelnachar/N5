import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { addVehicle, getVehicles } from '../actions/vehicleActions';
import { getAllPersons } from '../actions/personActions';
import { useNavigate } from 'react-router-dom';
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

const VehicleForm = () => {
  const [licensePlate, setLicensePlate] = useState('');
  const [brand, setBrand] = useState('');
  const [color, setColor] = useState('');
  const [owner, setOwner] = useState('');
  const [success, setSuccess] = useState('');
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const persons = useSelector(state => state.persons.persons);

  useEffect(() => {
    dispatch(getAllPersons());
  }, [dispatch]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const vehicle = { license_plate: licensePlate, brand, color, owner };
    await dispatch(addVehicle(vehicle));
    setSuccess('Vehicle created successfully!');
    dispatch(getVehicles());
  };

  return (
    <FormContainer>
      <h2>Cargar Vehículo</h2>
      {success && <SuccessMessage>{success}</SuccessMessage>}
      <Form onSubmit={handleSubmit}>
        <FormField>
          <label>License Plate:</label>
          <input
            type="text"
            value={licensePlate}
            onChange={(e) => setLicensePlate(e.target.value)}
          />
        </FormField>
        <FormField>
          <label>Brand:</label>
          <input
            type="text"
            value={brand}
            onChange={(e) => setBrand(e.target.value)}
          />
        </FormField>
        <FormField>
          <label>Color:</label>
          <input
            type="text"
            value={color}
            onChange={(e) => setColor(e.target.value)}
          />
        </FormField>
        <FormField>
          <label>Owner:</label>
          <select value={owner} onChange={(e) => setOwner(e.target.value)}>
            <option value="">Select Owner</option>
            {persons.map(person => (
              <option key={person.id} value={person.id}>
                {person.name}
              </option>
            ))}
          </select>
        </FormField>
        <button type="submit">Submit</button>
      </Form>
      <button type="button" onClick={() => navigate('/cargar_infraccion')}>
        Volver a Cargar Infracción
      </button>
    </FormContainer>
  );
};

export default VehicleForm;
