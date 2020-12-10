import { useHistory } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux'
import { signin } from '../redux/actions';

export default function Handle401(error, callback) {
  const history = useHistory();
  const dispatch = useDispatch();
  if (error.response && error.response.status === 401) {
    dispatch(signin(false, ''));
    history.push('/login');
  }
  else {
    callback()
  }
}