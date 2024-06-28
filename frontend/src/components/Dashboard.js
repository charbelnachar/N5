import React from 'react';
import { useNavigate } from 'react-router-dom';
import styled from 'styled-components';

const DashboardContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
`;

const Dashboard = () => {
  const navigate = useNavigate();
  
  const handleLogout = () => {
    localStorage.removeItem('token');
    
    navigate('/login');
  };


  return (
    <DashboardContainer>
      <h2>Dashboard</h2>
      <button onClick={() => navigate('/crud_personas')}>CRUD Personas</button>
      <button onClick={() => navigate('/crud_vehiculos')}>CRUD Vehículos</button>
      <button onClick={() => navigate('/crud_infracciones')}>CRUD Infracciones</button>
      <button onClick={() => navigate('/crud_oficiales')}>CRUD Oficiales</button>
      <button onClick={() => navigate('/generar_informe')}>Buscar Informe por Correo</button>
      <button onClick={handleLogout}>Logout</button>
      
    </DashboardContainer>
  );
};

export default Dashboard;
