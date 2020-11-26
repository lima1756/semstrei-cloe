import React from 'react';
import './App.css';
import Login from './components/pages/Login/Login';
import Users from './components/pages/Users/Users';
import Account from './components/pages/Account/Account';
import Dashboard from './components/pages/Dashboard/Dashboard';
import Graphs from './components/pages/Dashboard/Graphs';
import ControlTables from './components/pages/Dashboard/ControlTables';
import PasswordReset from './components/pages/PasswordReset/PasswordReset';
import EntryPoint from './components/pages/EntryPoint/EntryPoint';
import { SnackbarProvider } from 'notistack';
import ProtectedRoute from './components/ProtectedRoute';

import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';

function App() {

  return (
    <div className="App">
      <SnackbarProvider maxSnack={3}>
        <Router>
          <Switch>
            <ProtectedRoute path='/dashboard/resultTables' Component={Dashboard} />
            <ProtectedRoute path='/dashboard/graphs' Component={Graphs} />
            <ProtectedRoute path='/dashboard/controlTables' Component={ControlTables} />
            <ProtectedRoute path='/users' Component={Users} />
            <ProtectedRoute path='/account' Component={Account} />
            <Route path='/login' component={Login} />
            <Route exact path='/' component={EntryPoint} />
            <Route path={`/resetPassword/:id`} component={PasswordReset} />
            {/* <Route path='*' component={() => '404 NOT FOUND'}/> */}
          </Switch>
        </Router>
      </SnackbarProvider>
    </div>
  );
}

export default App;
