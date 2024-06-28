import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { getOfficers, addOfficer, updateOfficer, deleteOfficer } from '../actions/officerActions';
import { useNavigate } from 'react-router-dom';
import styled from 'styled-components';

const CrudContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
`;

const CrudOficiales = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const officers = useSelector(state => state.officers.officers) || [];
  const error = useSelector(state => state.officers.error);
  const [username, setUsername] = useState('');
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [identifier, setIdentifier] = useState('');
  const [selectedOfficer, setSelectedOfficer] = useState(null);

  useEffect(() => {
    dispatch(getOfficers());
  }, [dispatch]);

  const handleAdd = async () => {
    await dispatch(addOfficer({ username, name, email, password, identifier }));
    dispatch(getOfficers());
  };

  const handleUpdate = async () => {
    if (selectedOfficer) {
      await dispatch(updateOfficer(selectedOfficer.username, { username, name, email, password, identifier }));
      dispatch(getOfficers());
    }
  };

  const handleDelete = async (identifier) => {
    await dispatch(deleteOfficer(identifier));
    dispatch(getOfficers());
  };

  return (
    <CrudContainer>
      <h2>CRUD Oficiales</h2>
      {error && <div style={{ color: 'red' }}>{error}</div>}
      <input type="text" placeholder="Usuario" value={username} onChange={(e) => setUsername(e.target.value)} />
      <input type="text" placeholder="Nombre" value={name} onChange={(e) => setName(e.target.value)} />
      <input type="email" placeholder="Correo" value={email} onChange={(e) => setEmail(e.target.value)} />
      <input type="password" placeholder="Clave" value={password} onChange={(e) => setPassword(e.target.value)} />
      <input type="text" placeholder="Identificador" value={identifier} onChange={(e) => setIdentifier(e.target.value)} />
      <button onClick={handleAdd}>Agregar</button>
      <button onClick={handleUpdate}>Actualizar</button>
      <button onClick={() => navigate('/dashboard')}>Volver al Dashboard</button>
      <ul>
        {officers.map(officer => (
          <li key={officer.username}>
            Usuario:{officer.username} --- Nombre:{officer.name}----Correo:{officer.email}---Identificador: {officer.identifier})
            <button onClick={() => { setSelectedOfficer(officer); setUsername(officer.username); setName(officer.name); setEmail(officer.email); setIdentifier(officer.identifier); }}>Edit</button>
            <button onClick={() => handleDelete(officer.identifier)}>Delete</button>
          </li>
        ))}
      </ul>
    </CrudContainer>
  );
};

export default CrudOficiales;
