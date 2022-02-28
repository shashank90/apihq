import React from "react";
import styles from "./topbar.module.css";
import { useContext } from 'react';
import { Link } from 'react-router-dom';
import AuthContext from '../../store/auth-context';
import logo from "../../icon/ApiHQ.png"

export default function Topbar() {
  const authCtx = useContext(AuthContext);
  const isLoggedIn = authCtx.isLoggedIn;
  const logoutHandler = () => {
    authCtx.logout();
  };
  

  return (
    <div className={styles.topbar}>
        <div className={styles.logo}>
          <Link to='/'>
            <div> <img src={logo} width="100" height="50" /></div>
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
                {isLoggedIn && (
                  <li className={styles.item}>
                    <button className={styles.logout_btn} onClick={()=>logoutHandler()}>Logout</button>
                  </li>
                )}
              </ul>
            </nav>
        </div>
    </div>
  );
}
