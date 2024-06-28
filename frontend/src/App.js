import React, { useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import Login from './components/Login';
import InfractionForm from './components/InfractionForm';
import InfractionReport from './components/InfractionReport';
import PersonForm from './components/PersonForm';
import VehicleForm from './components/VehicleForm';
import Dashboard from './components/Dashboard';
import CrudPersonas from './components/CrudPersonas';
import CrudVehiculos from './components/CrudVehiculos';
import CrudInfracciones from './components/CrudInfracciones';
import CrudOficiales from './components/CrudOficiales';
import { loginSuccess } from './actions/authActions';

const PrivateRoute = ({ element: Element, ...rest }) => {
  const isAuthenticated = useSelector(state => state.auth.isAuthenticated);
  return isAuthenticated ? <Element {...rest} /> : <Navigate to="/login" />;
};

const App = () => {
  const dispatch = useDispatch();

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      dispatch(loginSuccess(token));
    }
  }, [dispatch]);

  return (
    <Router>
      <div>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/dashboard" element={<PrivateRoute element={Dashboard} />} />
          <Route path="/cargar_infraccion" element={<PrivateRoute element={InfractionForm} />} />
          <Route path="/generar_informe" element={<InfractionReport />} />
          <Route path="/cargar_persona" element={<PrivateRoute element={PersonForm} />} />
          <Route path="/cargar_vehiculo" element={<PrivateRoute element={VehicleForm} />} />
          <Route path="/crud_personas" element={<PrivateRoute element={CrudPersonas} />} />
          <Route path="/crud_vehiculos" element={<PrivateRoute element={CrudVehiculos} />} />
          <Route path="/crud_infracciones" element={<PrivateRoute element={CrudInfracciones} />} />
          <Route path="/crud_oficiales" element={<PrivateRoute element={CrudOficiales} />} />
          <Route path="/" element={<Navigate to="/login" />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
