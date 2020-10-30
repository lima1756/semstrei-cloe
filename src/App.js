import React from 'react';
import './App.css';
import Login from './components/Login';
import Users from './components/Users';
import Account from './components/Account';
import Dashboard from './components/Dashboard';
//import ProtectedRoute from './components/ProtectedRoute';

import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';

function App() {

  return (
    <div className="App">
      <Router>
        <Switch>
          <Route path='/dashboard' component={Dashboard} /> 
          <Route path='/users' component={Users} />
          <Route path='/account' component={Account} />
          <Route path='/login' component={Login} />
          <Route path='*' component={() => '404 NOT FOUND'}/>
        </Switch>
      </Router>
    </div>
  );
}

export default App;
