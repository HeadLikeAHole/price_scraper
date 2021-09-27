import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from 'react-router-dom';
import Navbar from './components/Navbar';

export default function App() {
  return (
    <Router>
      <Switch>
        <Route path="/">

        </Route>
        <Route path="/login">

        </Route>
      </Switch>
    </Router>
  );
}
