import Sidebar from "./layout/sidebar/Sidebar";
import Topbar from "./layout/topbar/Topbar";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import "./App.css";
import UserList from "./pages/userList/UserList";
import User from "./pages/user/User";
import NewUser from "./pages/newUser/NewUser";
import Issues from "./pages/findings/Issues";
import SpecEditor from "./pages/editor/SpecEditor";
import ApiDiscover from "./pages/discover/ApiDiscover";
import ApiRun from "./pages/run/ApiRun";
import ApiValidate from "./pages/validate/ApiValidate";

function App() {
  return (
    <Router>
      <Topbar />
      <div className="container">
        <Sidebar />
        <Switch>
          <Route exact path="/">
            <ApiDiscover />
          </Route>
          <Route exact path="/users">
            <UserList />
          </Route>
          <Route exact path="/user/:userId">
            <User />
          </Route>
          <Route exact path="/newUser">
            <NewUser />
          </Route>
          <Route exact path="/apis">
            <ApiDiscover />
          </Route>
          <Route exact path="/apis/spec/editor">
            <SpecEditor />
          </Route>
          <Route exact path="/apis/spec/editor/:specId">
            <SpecEditor />
          </Route>
          <Route exact path="/apis/validate">
            <ApiValidate />
          </Route>
          <Route exact path="/apis/run">
            <ApiRun />
          </Route>
          <Route exact path="/apis/run/issues/:runId">
            <Issues />
          </Route>
        </Switch>
      </div>
    </Router>
  );
}

export default App;
