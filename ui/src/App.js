import Sidebar from "./layout/sidebar/Sidebar";
import React, { useContext } from "react";
import Topbar from "./layout/topbar/Topbar";
import Bottombar from "./layout/bottombar/Bottombar";
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
import ApiTest from "./pages/test/ApiTest";
import MsgList from "./pages/request/MsgList";
import Auth from "./pages/auth/Auth";
import Landing from "./pages/landing/Landing";
import AuthContext from "./store/auth-context";
import RequestEditor from "./components/requestEditor/RequestEditor";

function App() {
  const authCtx = useContext(AuthContext);

  return (
    <Router>
      <Topbar />
      <Switch>
        {!authCtx.isLoggedIn && (
          <Route exact path="/" component={LandingContainer} />
        )}
        {!authCtx.isLoggedIn && (
          <Route exact path="/auth/:authType" component={LoginContainer} />
        )}
        {authCtx.isLoggedIn && <Route component={DefaultContainer} />}
        {!authCtx.isLoggedIn && <Redirect to="/" />}
      </Switch>
    </Router>
  );
}

const LandingContainer = () => (
  <React.Fragment>
    <div className="container">
      <Route path="/" component={Landing} />
    </div>
    <Bottombar />
  </React.Fragment>
);

const LoginContainer = () => (
  <React.Fragment>
    <div className="container">
      <Route path="/auth/:authType" component={Auth} />
    </div>
    <Bottombar />
  </React.Fragment>
);

const DefaultContainer = () => (
  <div className="container">
    <Sidebar />
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
      <RequestEditor />
    </Route>
    <Route exact path="/apis/test">
      <ApiTest />
    </Route>
    <Route exact path="/apis/test/issues/:runId">
      <Issues />
    </Route>
    <Route exact path="/apis/test/requests/:runId">
      <MsgList />
    </Route>
  </div>
);

export default App;
