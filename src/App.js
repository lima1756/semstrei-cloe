import React from 'react';
import './App.css';
import Login from './components/pages/Login/Login';
import Users from './components/pages/Users/Users';
import Account from './components/pages/Account/Account';
import Dashboard from './components/pages/Dashboard/Dashboard';
import PasswordReset from './components/pages/PasswordReset/PasswordReset';
import {SnackbarProvider} from 'notistack';
//import ProtectedRoute from './components/ProtectedRoute';

import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';

function App() {

  return (
    <div className="App">
      <SnackbarProvider maxSnack={3}>
      <Router>
        <Switch>
          <Route path='/dashboard' component={Dashboard} /> 
          <Route path='/users' component={Users} />
          <Route path='/account' component={Account} />
          <Route path='/login' component={Login} />
          <Route path={`/resetPassword/:id`} component={PasswordReset} />
          {/* <Route path='*' component={() => '404 NOT FOUND'}/> */}
        </Switch>
      </Router>
      </SnackbarProvider>
    </div>
  );
}

export default App;
