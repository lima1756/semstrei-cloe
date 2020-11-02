const IS_LOGGED = { logged: false, token: '' };

const loggedReducer = (state = IS_LOGGED , action ) => {
    switch(action.type){
        case 'SIGNIN':
            return {
                logged: action.logged,
                token: action.token,
            };
        default: return state
    }
}


export default loggedReducer;