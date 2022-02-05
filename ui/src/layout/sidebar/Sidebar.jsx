import "./sidebar.css";
import { Link } from "react-router-dom";

export default function Sidebar() {
  return (
    <div className="sidebar">
      <div className="sidebarWrapper">
        {/* <div className="sidebarMenu">
          <h3 className="sidebarTitle">Dashboard</h3>
          <ul className="sidebarList">
            <Link to="/" className="link">
              <li className="sidebarListItem active">Home</li>
            </Link>
          </ul>
        </div> */}
        <div className="sidebarMenu">
          <h3 className="sidebarTitle">APIs</h3>
          <ul className="sidebarList">
            {/* TODO: Uncomment users later */}
            {/* <Link to="/users" className="link">
              <li className="sidebarListItem">
                <PermIdentity className="sidebarIcon" />
                Users
              </li>
            </Link> */}

            <Link to="/apis" className="link">
              <li className="sidebarListItem">Discover</li>
            </Link>
            <Link to="/apis/run" className="link">
              <li className="sidebarListItem">Run</li>
            </Link>
          </ul>
        </div>
        {/* <div className="sidebarMenu">
          <h3 className="sidebarTitle">Findings</h3>
          <ul className="sidebarList">
            <Link to="/vulns" className="link">
              <li className="sidebarListItem">Issues</li>
            </Link>
          </ul>
        </div> */}
      </div>
    </div>
  );
}
