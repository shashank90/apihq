import Sidebar from "./layout/sidebar/Sidebar";
import { useContext } from "react";
import Topbar from "./layout/topbar/Topbar";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Redirect,
} from "react-router-dom";
import "./App.css";
import Issues from "./pages/findings/Issues";
import SpecEditor from "./pages/editor/SpecEditor";
import ApiDiscover from "./pages/discover/ApiDiscover";
import ApiRun from "./pages/run/ApiRun";
import Auth from "./pages/auth/Auth";
import AuthContext from "./store/auth-context";

function App() {
  const authCtx = useContext(AuthContext);

  return (
    <Router>
      <Topbar />
      <Switch>
        {!authCtx.isLoggedIn && (
          <Route exact path="/login" component={LoginContainer} />
        )}
        {authCtx.isLoggedIn && <Route component={DefaultContainer} />}
        {!authCtx.isLoggedIn && <Redirect to="/login" />}
      </Switch>
    </Router>
  );
}

const LoginContainer = () => (
  <div className="container">
    <Route path="/login" component={Auth} />
  </div>
);

const DefaultContainer = () => (
  <div className="container">
    <Sidebar />
    <Route exact path="/">
      <ApiDiscover />
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
    <Route exact path="/apis/run">
      <ApiRun />
    </Route>
    <Route exact path="/apis/run/issues/:runId">
      <Issues />
    </Route>
  </div>
);

export default App;
