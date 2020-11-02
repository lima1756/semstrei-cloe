export const userinformation = (admin, newUser, name, mail, phone, role, userId) => {
    return{
        type: 'USERINFORMATION',
        admin: admin,
        newUser: newUser,
        name: name,
        mail: mail,
        phone: phone,
        role: role,
        userId: userId
    }
}

export const signin = (logged, token) => {
    return{
        type: 'SIGNIN',
        logged: logged,
        token: token,
    }
}