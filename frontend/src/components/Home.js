import runningMan from '../img/running-man.png';
import dotMap from '../img/dot-map.png';

export default function Home() {
  return (
    <main>
      <section className="main-first">
        <div className="main-first-text">
          <h1 className="main-first-title">
            An easy way to keep track of prices on your favorite online stores
          </h1>
          <p className="main-first-description">
            Just save the link to the product you wish to buy and get an email when the price drops to the amount you specified
          </p>
        </div>
        <div className="running-man">
          <img src={runningMan} alt="" />
        </div>
      </section>
      <section className="main-second">
        <h1 className="main-second-title">
          To get started just create an account
        </h1>
        <article>
          <h2></h2>
          <p></p>
        </article>
        <article>
          <h2></h2>
          <p></p>
        </article>
        <article>
          <h2></h2>
          <p></p>
        </article>
      </section>
    </main>
  );
}