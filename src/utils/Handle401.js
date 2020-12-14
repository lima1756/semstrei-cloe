import { signin } from '../redux/actions';

export default function Handle401(error, history, dispatch, callback) {
  if (error.response && error.response.status === 401) {
    dispatch(signin(false, ''));
    history.push('/login');
  }
  else if (callback != null) {
    callback()
  }
}