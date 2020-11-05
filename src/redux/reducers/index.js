import loggedReducer from './isLogged';
import userReducer from './userInformation';
import isOpen from './isOpen';
import { combineReducers } from 'redux'; 
import { persistReducer } from 'redux-persist';
import storage from 'redux-persist/lib/storage';

const persistConfig = {
    key: 'root',
    storage,
    whitelist: ['user', 'logged', 'openDrawer']
};

const allReducers = combineReducers({
    logged: loggedReducer,
    user: userReducer,
    openDrawer: isOpen,
})

export default persistReducer(persistConfig, allReducers);