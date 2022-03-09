import React, { useState, useEffect, useContext } from "react";
import { useHistory, useLocation, Redirect } from "react-router-dom";
import ProxyMessagesContext from "../../store/proxymsg-context";
import Message from "../../components/common/Message";

export default function MsgDetails() {
  const proxyMessagesCtx = useContext(ProxyMessagesContext);
  const contextData = proxyMessagesCtx.contextData;
  const [editable, setEditable] = useState(false);
  const [msgDetails, setMsgDetails] = useState({
    reqHeader: "",
    reqBody: "",
    resHeader: "",
    resBody: "",
  });
  const location = useLocation();

  // Get action from calling Link wrapped component
  const { action, msgId } = location.state;

  useEffect(() => {
    if (action === "edit") {
      setEditable(true);
    }

    //Get Context and set Message details
    const msgObj = contextData.getMessage(msgId);

    const uri = msgObj.request.uri;
    const reqHeader = JSON.stringify(msgObj.request.headers);
    const reqBody = JSON.stringify(msgObj.request.body);
    const resHeader = JSON.stringify(msgObj.response.headers);
    const resBody = JSON.stringify(msgObj.response.body);
    setMsgDetails({
      uri: uri,
      reqHeader: reqHeader,
      reqBody: xreqBody,
      resHeader: resHeader,
      resBody: resBody,
    });
  }, [action]);

  return <Message msgDetails={msgDetails} editable={editable} />;
}
