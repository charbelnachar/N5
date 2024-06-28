import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { getInfractions, addInfraction, updateInfraction, deleteInfraction } from '../actions/infractionActions';
import { getVehicles } from '../actions/vehicleActions';
import { useNavigate } from 'react-router-dom';
import styled from 'styled-components';
import { format } from 'date-fns';

const CrudContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
`;

const CrudInfracciones = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const infractions = useSelector(state => state.infractions.infractions) || [];
  const vehicles = useSelector(state => state.vehicles.vehicles) || [];
  const [licensePlate, setLicensePlate] = useState('');
  const [timestamp, setTimestamp] = useState('');
  const [comments, setComments] = useState('');
  const [selectedInfraction, setSelectedInfraction] = useState(null);

  useEffect(() => {
    dispatch(getInfractions());
    dispatch(getVehicles());
  }, [dispatch]);

  const handleAdd = async () => {
    await dispatch(addInfraction({ license_plate: licensePlate, timestamp, comments }));
    dispatch(getInfractions());
  };

  const handleUpdate = async () => {
    if (selectedInfraction) {
      await dispatch(updateInfraction(selectedInfraction.id, { license_plate: licensePlate, timestamp, comments }));
      dispatch(getInfractions());
    }
  };

  const handleDelete = async (id) => {
    await dispatch(deleteInfraction(id));
    dispatch(getInfractions());
  };

  return (
    <CrudContainer>
      <h2>CRUD Infracciones</h2>
      <select value={licensePlate} onChange={(e) => setLicensePlate(e.target.value)}>
        <option value="">Seleccione placa </option>
        {vehicles.map(vehicle => (
          <option key={vehicle.id} value={vehicle.license_plate}>{vehicle.license_plate}</option>
        ))}
      </select>
      <input type="datetime-local" value={timestamp} onChange={(e) => setTimestamp(e.target.value)} />
      <input type="text" placeholder="Comments" value={comments} onChange={(e) => setComments(e.target.value)} />
      <button onClick={handleAdd}>Agregar</button>
      <button onClick={handleUpdate}>Actualizar</button>
      <button onClick={() => navigate('/dashboard')}>Volver al Dashboard</button>
      <ul>
        {infractions.map(infraction => (
          <li key={infraction.id}>
            placa: {infraction.vehicle.license_plate} ---- hora: {infraction.timestamp ? format(new Date(infraction.timestamp), 'yyyy-MM-dd HH:mm'): ''} ----  infraccion: {infraction.comments}
            <button onClick={() => { console.log(infraction); setSelectedInfraction(infraction);
             setLicensePlate(infraction.vehicle.license_plate);  
             setTimestamp(infraction.timestamp ? new Date(infraction.timestamp).toISOString().slice(0,16) : ''); 
             setComments(infraction.comments); }}>Edit</button>
            <button onClick={() => handleDelete(infraction.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </CrudContainer>
  );
};

export default CrudInfracciones;
