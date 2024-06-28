import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { getVehicles, addVehicle, updateVehicle, deleteVehicle } from '../actions/vehicleActions';
import { getAllPersons } from '../actions/personActions';
import { useNavigate } from 'react-router-dom';
import styled from 'styled-components';

const CrudContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
`;

const CrudVehiculos = () => {
 
  const setVehiculos = [];
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const vehicles = useSelector(state => state.vehicles.vehicles) || [];
  const persons = useSelector(state => state.persons.persons) || [];
  const [licensePlate, setLicensePlate] = useState('');
  const [brand, setBrand] = useState('');
  const [color, setColor] = useState('');
  const [owner, setOwner] = useState('');
  const [selectedVehicle, setSelectedVehicle] = useState(null);

  useEffect(() => {
    dispatch(getVehicles());
    dispatch(getAllPersons());
  }, [dispatch]);

  const handleAdd = async () => {
    await dispatch(addVehicle({ license_plate: licensePlate, brand, color, owner }));
    dispatch(getVehicles());
    setSelectedVehicle(null);
    setLicensePlate('');
    setBrand('');
    setColor('');
    setOwner('');
  };

  const handleUpdate = async () => {
    if (selectedVehicle) {
      await dispatch(updateVehicle(selectedVehicle.license_plate, { license_plate: licensePlate, brand, color, owner }));
     
      setSelectedVehicle(null);
    setLicensePlate('');
    setBrand('');
    setColor('');
    setOwner('');
     dispatch(getVehicles());
    }
  };

  const handleDelete = async (licensePlate) => {
    await dispatch(deleteVehicle(licensePlate));
    dispatch(getVehicles());
    setSelectedVehicle(null);
    setLicensePlate('');
    setBrand('');
    setColor('');
    setOwner('');
  };

  return (
    <CrudContainer>
      <h2>CRUD Vehículos</h2>
      <input type="text" placeholder="Placa" value={licensePlate} onChange={(e) => setLicensePlate(e.target.value)} />
      <input type="text" placeholder="Modelo" value={brand} onChange={(e) => setBrand(e.target.value)} />
      <input type="text" placeholder="Color" value={color} onChange={(e) => setColor(e.target.value)} />
      <select value={owner} onChange={(e) => setOwner(e.target.value)}>
        <option value="">Seleccionar dueño</option>
        {persons.map(person => (
          <option key={person.id} value={person.id}>{person.name}</option>
        ))}
      </select>
      <button onClick={handleAdd}>Agregar</button>
      <button onClick={handleUpdate}>Actualizar</button>
      <button onClick={() => navigate('/dashboard')}>Volver al Dashboard</button>
      <ul>
        {vehicles.map(vehicle => (
          <li key={vehicle.id}>
            Dueño: {vehicle.owner.name}  Placa: {vehicle.license_plate} ( Modelo: {vehicle.brand},  Color: {vehicle.color})
            <button onClick={() => { setSelectedVehicle(vehicle); setLicensePlate(vehicle.license_plate); setBrand(vehicle.brand); setColor(vehicle.color); setOwner(vehicle.owner.id);   }}>  Edit</button>
            <button onClick={() => handleDelete(vehicle.license_plate)}>Delete</button>
          </li>
        ))}
      </ul>
    </CrudContainer>
  );
};

export default CrudVehiculos;
