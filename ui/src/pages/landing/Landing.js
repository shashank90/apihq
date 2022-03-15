import React from "react";
import styles from "./landingPage.module.css";
import { Link } from "react-router-dom";
export default function Landing() {
  return (
    <div className={styles.wrap}>
      <div className={styles.title}>Introducing ApiHome</div>
      <div className={styles.gridWrap}>
        <div className={styles.item}>
          <div className={styles.benefitTitle}>Home of API</div>
          <div className={styles.benefitExpl}>
            <ul className={styles.listStyle}>
              <li className={styles.lineItemStyle}>Discovery</li>
              <li className={styles.lineItemStyle}>Design</li>
              <li className={styles.lineItemStyle}>Contract Testing</li>
              <li className={styles.lineItemStyle}>Request Fuzzing</li>
            </ul>
          </div>
        </div>
        <div className={styles.item}>
          <div className={styles.benefitTitle}>Why ApiHome?</div>
          <div className={styles.benefitExpl}>
            <ul className={styles.listStyle}>
              <li className={styles.lineItemStyle}>
                Easy to maintain documentation
              </li>
              <li className={styles.lineItemStyle}>
                Auto generated test cases
              </li>
              <li className={styles.lineItemStyle}>Uncover Security flaws</li>
              <li className={styles.lineItemStyle}>
                Get up and testing in minutes
              </li>
            </ul>
          </div>
        </div>
        {/* <div className="item">
          <div className="benefit-title">Benefit of the product</div>
          <div className="benefit-expl">
            Explanation of the benefit that is quite long, long, long, long.
          </div>
        </div> */}
        {/* <div className="item">
        <div className="benefit-title">Amazing benefit of the product</div>
        <div className="benefit-expl">Explanation of the benefit.</div>
      </div> */}
      </div>
      <div className={styles.signUpContainer}>
        <Link to="/auth/signup">
          <button className={styles.signUpBtn}>
            Get Started in 30 seconds
          </button>
        </Link>
      </div>
    </div>
  );
}
