import { useState } from "react";
import "./msgDetails.css";
import Buttons from "../../components/common/Buttons";

export default function Message(props) {
  const editable = props.editable;
  const msgDetails = props.msgDetails;
  const hideMessage = props.hideMessage;

  const [uri, setUri] = useState(msgDetails.url);
  const [reqHeader, setReqHeader] = useState(msgDetails.reqHeader);
  const [reqBody, setReqBody] = useState(msgDetails.reqBody);
  const [resHeader, setResHeader] = useState(msgDetails.resHeader);
  const [resBody, setResBody] = useState(msgDetails.resBody);
  const [remarks, setRemarks] = useState();

  const isBackBtnVisible = true;

  const handleOnBack = () => {
    //Do nothing
    // Ensure this is passed from calling the component. Or handle gracefully
    props.showRequest(false);
  };

  function handleURIChange(event) {
    setUri(event.target.value);
  }
  function handleReqHeaderChange(event) {
    setReqHeader(event.target.value);
  }
  function handleReqBodyChange(event) {
    setReqBody(event.target.value);
  }
  function handleResHeaderChange(event) {
    setResHeader(event.target.value);
  }
  function handleResBodyChange(event) {
    setResBody(event.target.value);
  }
  function handleRemarksChange(event) {
    setRemarks(event.target.value);
  }

  return (
    <div>
      <div>
        <Buttons
          isBackBtnVisible={isBackBtnVisible}
          onBackHandle={handleOnBack}
        />
      </div>
      <div className="msgWrapper">
        <div className="msgGridWrapper">
          <div className="request-uri-label">
            <label>URI</label>
          </div>
          <input
            className="request-uri"
            disabled={!editable}
            value={uri}
            onChange={handleURIChange}
          />
          <div className="request-header-label">
            <label>Request Header</label>
          </div>
          <textarea
            className="request-header"
            disabled={!editable}
            value={reqHeader}
            onChange={handleReqHeaderChange}
          />
          <div className="request-body-label">
            <label>Request Body</label>
          </div>
          <textarea
            className="request-body"
            disabled={!editable}
            value={reqBody}
            onChange={handleReqBodyChange}
          />
          <div className="response-header-label">
            <label>Response Header</label>
          </div>
          <textarea
            className="response-header"
            disabled={!editable}
            value={resHeader}
            onChange={handleResHeaderChange}
          />
          <div className="response-body-label">
            <label>Response Body</label>
          </div>
          <textarea
            className="response-body"
            disabled={!editable}
            value={resBody}
            onChange={handleResBodyChange}
          />
        </div>
      </div>
    </div>
  );
}
