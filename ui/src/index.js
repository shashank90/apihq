import React from "react";
import ReactDOM from "react-dom";
import { ProxyMessagesContextProvider } from "./store/proxymsg-context";
import { BuiltinTestsContextProvider } from "./store/builtintests-context";
import { UserTestsContextProvider } from "./store/usertests-context";
import { TargetListContextProvider } from "./store/targetlist-context";
import { VulnsContextProvider } from "./store/vulns-context";
import App from "./App";

ReactDOM.render(
  <ProxyMessagesContextProvider>
    <BuiltinTestsContextProvider>
      <UserTestsContextProvider>
        <TargetListContextProvider>
          <VulnsContextProvider>
            <React.StrictMode>
              <App />
            </React.StrictMode>
          </VulnsContextProvider>
        </TargetListContextProvider>
      </UserTestsContextProvider>
    </BuiltinTestsContextProvider>
  </ProxyMessagesContextProvider>,
  document.getElementById("root")
);
