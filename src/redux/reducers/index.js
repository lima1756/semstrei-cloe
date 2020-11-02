import loggedReducer from './isLogged';
import userReducer from './userInformation';
import { combineReducers } from 'redux'; 
import { persistReducer } from 'redux-persist';
import storage from 'redux-persist/lib/storage';

const persistConfig = {
    key: 'root',
    storage,
    whitelist: ['user', 'logged']
};

const allReducers = combineReducers({
    logged: loggedReducer,
    user: userReducer
})

export default persistReducer(persistConfig, allReducers);