import { Routes, Route } from 'react-router-dom';
import AdminManage from '../components/AdminManage.js';
import PrivateRoute from './PrivateRoute.js';
import Login from '../components/Login.js';

const AppRoutes = () => {
    return (
        <Routes>
            <Route path="/login" element={<Login />} />
            <Route element={<PrivateRoute />}>
                <Route path="/admin" element={<AdminManage />} />
            </Route>
        </Routes>
    );
}

export default AppRoutes;
