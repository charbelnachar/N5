import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { getAllPersons, addPerson, updatePerson, deletePerson } from '../actions/personActions';
import { useNavigate } from 'react-router-dom';
import styled from 'styled-components';

const CrudContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
`;

const CrudPersonas = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const persons = useSelector(state => state.persons.persons);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const error = useSelector(state => state.persons.error);

  const [selectedPerson, setSelectedPerson] = useState(null);

  useEffect(() => {
    dispatch(getAllPersons());
  }, [dispatch]);

  const handleAdd = async () => {    
    await dispatch(addPerson({ name, email }));
    dispatch(getAllPersons());
  };

  const handleUpdate = async () => {
    if (selectedPerson) {
      await dispatch(updatePerson(selectedPerson.id, { name, email }));
      dispatch(getAllPersons());
    }
  };

  const handleDelete = async (id) => {
    await dispatch(deletePerson(id));
    dispatch(getAllPersons());
  };

  return (
    <CrudContainer>
      <h2>CRUD Personas</h2>
     
      <input type="text" placeholder="Nombre" value={name} onChange={(e) => setName(e.target.value)} />
      <input type="email" placeholder="Correo" value={email} onChange={(e) => setEmail(e.target.value)} />
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <button onClick={handleAdd}>Agregar</button>
      <button onClick={handleUpdate}>Actualizar</button>
      <button onClick={() => navigate('/dashboard')}>Volver al Dashboard</button>
      <ul>
        {persons.map(person => (
          <li key={person.id}>
            Nombre: {person.name} -- Correo: {person.email}
            <button onClick={() => { setSelectedPerson(person); setName(person.name);setEmail(person.email); }}>Edit</button>
            <button onClick={() => handleDelete(person.id)}>Borrar</button>
          </li>
        ))}
      </ul>
    </CrudContainer>
  );
};

export default CrudPersonas;
