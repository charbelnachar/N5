import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { login } from '../actions/authActions';
import styled from 'styled-components';

const LoginContainer = styled.div`
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

const ErrorMessage = styled.div`
  color: red;
  margin-bottom: 10px;
`;

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const error = useSelector(state => "Usuario o clave incorrectos");

  const handleSubmit = async (e) => {
    e.preventDefault();
    const success = await dispatch(login(username, password));
    if (success) {
      navigate('/dashboard');
    }
  };

  return (
    <LoginContainer>
      <h2>Login</h2>
      <Form onSubmit={handleSubmit}>
        {error && <ErrorMessage>{error}</ErrorMessage>}
        <FormField>
          <label>Usuario:</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </FormField>
        <FormField>
          <label>Clave:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </FormField>
        <button type="submit">Login</button>
      </Form>
      <button onClick={() => navigate('/generar_informe')}>Generar Informe</button>
    </LoginContainer>
  );
};

export default Login;
