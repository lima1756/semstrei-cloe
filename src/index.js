import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import './index.css';
import App from './App';
import * as serviceWorker from './serviceWorker';
import  { createStore } from 'redux';
import allReducer from './redux/reducers'
import { persistStore } from 'redux-persist'
import { PersistGate } from 'redux-persist/integration/react'

const store = createStore(
  allReducer, 
  window.__REDUX_DEVTOOLS_EXTENSION__ && window.__REDUX_DEVTOOLS_EXTENSION__()
  );

const persistor = persistStore(store);

ReactDOM.render(
  <React.StrictMode>
    <Provider store={ store }>
      <PersistGate persistor={persistor}>
      <App />
      </PersistGate>
    </Provider>
  </React.StrictMode>,
  document.getElementById('root')
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
