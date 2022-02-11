import React from "react";
import styles from "./topbar.module.css";
import { useContext } from 'react';
import { Link } from 'react-router-dom';
import AuthContext from '../../store/auth-context';

export default function Topbar() {
  const authCtx = useContext(AuthContext);
  const isLoggedIn = authCtx.isLoggedIn;

  return (
    <div className={styles.topbar}>
        <div className={styles.logo}>
          <Link to='/'>
            <div>ApiHQ</div>
          </Link>
        </div>
        <div className={styles.topbarMenuContainer}>
            <nav>
              <ul className={styles.list}>
                {!isLoggedIn && (
                  <li className={styles.item}>
                    <Link to='/login'>Login</Link>
                  </li>
                )}
                {/* {isLoggedIn && (
                  <li>
                    <Link to='/profile'>Profile</Link>
                  </li>
                )} */}
                {isLoggedIn && (
                  <li className={styles.item}>
                    <button className={styles.logout_btn}>Logout</button>
                  </li>
                )}
              </ul>
            </nav>
        </div>
    </div>
  );
}
