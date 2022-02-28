import React from "react";
import styles from "./bottombar.module.css";
import { useContext } from "react";
import { Link } from "react-router-dom";
// import AuthContext from "../../store/auth-context";

export default function Topbar() {
  //   const authCtx = useContext(AuthContext);
  //   const isLoggedIn = authCtx.isLoggedIn;

  return (
    <div className={styles.bottombar}>
      <div className={styles.bottombarContent}>
        <div className={styles.supportMessage}>
          For support queries write to: contactus@cymitra.com.
          <p>
            For more information checkout:
            <a href="http://cymitra.com">Cymitra</a>
          </p>
        </div>
      </div>
    </div>
  );
}
