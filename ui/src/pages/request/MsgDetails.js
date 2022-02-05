import React, { useState, useEffect, useContext } from "react";
import { useHistory, useLocation, Redirect } from "react-router-dom";
import ProxyMessagesContext from "../../store/proxymsg-context";
import Message from "../../components/common/Message";

export default function MsgDetails() {
  console.log("Inside MsgDetails");

  const proxyMessagesCtx = useContext(ProxyMessagesContext);
  const contextData = proxyMessagesCtx.contextData;
  const [editable, setEditable] = useState(false);
  const [isRedirectURI, setIsRedirectURI] = useState(false);
  const [redirectURI, setRedirectURI] = useState("");
  const [msgDetails, setMsgDetails] = useState({
    reqHeader: "",
    reqBody: "",
    resHeader: "",
    resBody: "",
  });
  const location = useLocation();

  // Get action from calling Link wrapped component
  const { action, msgId } = location.state;
  console.log("Action: " + action);
  console.log("msgId: " + msgId);

  useEffect(() => {
    if (action === "edit") {
      setEditable(true);
    }

    //Get Context and set Message details
    const msgObj = contextData.getMessage(msgId);

    //TODO: Fix this block. Need to redirect in case of page refresh or direct URI fetch attempt on browser
    if (!msgObj) {
      console.log(
        "Msg could not be found. Redirect back to list of proxy messages"
      );
      setIsRedirectURI(true);
      setRedirectURI("/proxy/messages");
    }
    //

    console.log(msgObj);
    const uri = msgObj.request.uri;
    const reqHeader = JSON.stringify(msgObj.request.headers);
    const reqBody = JSON.stringify(msgObj.request.body);
    const resHeader = JSON.stringify(msgObj.response.headers);
    const resBody = JSON.stringify(msgObj.response.body);
    setMsgDetails({
      uri: uri,
      reqHeader: reqHeader,
      reqBody: reqBody,
      resHeader: resHeader,
      resBody: resBody,
    });
  }, [action]);

  console.log("IsRedirectURI " + isRedirectURI);
  console.log("SetRedirectURI " + redirectURI);

  return <Message msgDetails={msgDetails} editable={editable} />;
}
