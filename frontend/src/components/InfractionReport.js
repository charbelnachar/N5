import React, { useState } from 'react';
import { format } from 'date-fns';
import styled from 'styled-components';
import { useNavigate } from 'react-router-dom';
import api from '../api';
const ReportContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
`;


const InfractionReport = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [report, setReport] = useState(null);


  const handleLogout = () => {
    localStorage.removeItem('token');
    
    navigate('/login');
  };

  const handleGenerateReport = async () => {
    try {
      const response = await api.get(`/generar_informe/?email=${email}`);
      setReport(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <ReportContainer>
      <h2> buscar infracción por correo Correo</h2>
      <input
        type="email"
        placeholder="Enter email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <button onClick={handleGenerateReport}>Generate Report</button>
      {report && (
        <div>
          <h3>Reporte</h3>
          <ul>
            {report.map(item => (
              <li key={item.id}>
               Placa: {item.vehicle.license_plate} ---- Hora : {format(new Date(item.timestamp), 'yyyy-MM-dd HH:mm')}---- Comentario: {item.comments} ---- Officer: {item.officer.name}
              </li>
            ))}
          </ul>
        </div>
      )}
      <button onClick={() => navigate('/dashboard')}>Volver al Dashboard</button>
      <button onClick={handleLogout}>Logout</button>
    </ReportContainer>
  );
};

export default InfractionReport;
