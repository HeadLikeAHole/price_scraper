import logo from '../img/logo.png';

export default function Navbar() {
  return (
    <nav>
      <div className="logo">
        <img src={logo} alt="" title="Price Scraper"/>
      </div>
      <div className="nav-buttons">
        <button className="btn btn-nav">log in</button>
        <button className="btn btn-nav">sign up</button>
      </div>
    </nav>
  );
}