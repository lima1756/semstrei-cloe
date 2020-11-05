const IS_OPEN  = { menuDrawer : true, };

const isOpenReducer = (state = IS_OPEN, action) => {
    switch(action.type){
        case 'ISOPEN':
            return{
                menuDrawer : action.menuDrawer,
            };
        default: return state
    }
}

export default isOpenReducer;