import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { addInfraction } from '../actions/infractionActions';
import { getVehicles } from '../actions/vehicleActions';
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

const InfractionForm = () => {
  const [timestamp, setTimestamp] = useState('');
  const [comments, setComments] = useState('');
  const [selectedVehicle, setSelectedVehicle] = useState('');
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const vehicles = useSelector(state => state.vehicles.vehicles);

  useEffect(() => {
    dispatch(getVehicles());
  }, [dispatch]);

  const handleSubmit = (e) => {
    e.preventDefault();
    const infraction = { 
      license_plate: selectedVehicle, 
      timestamp, 
      comments 
    };
    dispatch(addInfraction(infraction));
  };

  return (
    <FormContainer>
      <h2>Cargar Infracción</h2>
      <Form onSubmit={handleSubmit}>
        <FormField>
          <label>License Plate:</label>
          {vehicles.length > 0 ? (
            <select 
              value={selectedVehicle} 
              onChange={(e) => setSelectedVehicle(e.target.value)}
            >
              <option value="">Select a vehicle</option>
              {vehicles.map(vehicle => (
                <option key={vehicle.id} value={vehicle.license_plate}>
                  {vehicle.license_plate}
                </option>
              ))}
            </select>
          ) : (
            <div>No vehicles available.</div>
          )}
        </FormField>
        <FormField>
          <label>Timestamp:</label>
          <input
            type="datetime-local"
            value={timestamp}
            onChange={(e) => setTimestamp(e.target.value)}
          />
        </FormField>
        <FormField>
          <label>Comments:</label>
          <input
            type="text"
            value={comments}
            onChange={(e) => setComments(e.target.value)}
          />
        </FormField>
        <button type="submit">Submit</button>
      </Form>
      <button type="button" onClick={() => navigate('/cargar_vehiculo')}>
        Agregar vehiculo
      </button>
      <button type="button" onClick={() => navigate('/dashboard')}>
        Volver al Dashboard
      </button>
    </FormContainer>
  );
};

export default InfractionForm;
