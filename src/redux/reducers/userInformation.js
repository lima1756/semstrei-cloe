const USER_INFORMATION = { admin: false, newUser: false, name: '', mail: '', phone: '', role: -1, userId: -1 };

const informationReducer = (state = USER_INFORMATION, action) => {
    switch(action.type){
        case 'USERINFORMATION':
            return {
                admin: action.admin,
                newUser: action.newUser,
                name: action.name,
                mail: action.mail,
                phone: action.phone,
                role: action.role,
                userId: action.userId,
            };
        default: return state;
    }
}

export default informationReducer;