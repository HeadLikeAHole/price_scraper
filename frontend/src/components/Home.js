import runningMan from '../img/running-man.png';
import dotMap from '../img/dot-map.png';

export default function Home() {
  return (
    <main>
      <section className="main-first">
        <div className="main-first-text">
          <h1 className="main-first-title">
            An easy way to keep track of <span>prices</span> on your favorite online <span>stores</span>
          </h1>
          <p className="main-first-description">
            Save the link to the product you wish to buy and get an email when the price drops to the amount you specified
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
        <div className="articles">
          <article>
            <h2 className="article-title">Easy to sign up</h2>
            <p className="article-description">Just provide your email and password and you're good to go</p>
          </article>
          <article>
            <h2 className="article-title">Simple to use</h2>
            <p className="article-description">Find a product you want to buy, save the link to it and set a desired price</p>
          </article>
          <article>
            <h2 className="article-title">Constant updates</h2>
            <p className="article-description">If the price drops to the desired one get a notifying email within an hour</p>
          </article>
        </div>
      </section>
    </main>
  );
}