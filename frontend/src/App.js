import {
  BrowserRouter as Router,
  Switch,
  Route
} from 'react-router-dom';
import Navbar from './components/Navbar';

export default function App() {
  return (
    <Router>
      <Navbar />
      <Switch>
        <Route path="/">

        </Route>
        <Route path="/login">

        </Route>
      </Switch>
    </Router>
  );
}
