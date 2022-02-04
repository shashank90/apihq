import { useState } from "react";
import { useHistory } from "react-router-dom";
import TestBottombar from "../../layout/testbottombar/TestBottombar";
import "./msgDetails.css";

export default function Message(props) {
  const editable = props.editable;
  const msgDetails = props.msgDetails;
  const hideMessage = props.hideMessage;
  let fuzzRequestPayload = false;
  let fuzzRequestURI = false;
  let reviewRequest = false;

  const nouns = props.nouns;
  const attributes = props.attributes;
  fuzzRequestPayload = props.fuzzRequestPayload;
  fuzzRequestURI = props.fuzzRequestURI;
  reviewRequest = props.reviewRequest;

  const [uri, setUri] = useState(msgDetails.uri);
  const [reqHeader, setReqHeader] = useState(msgDetails.reqHeader);
  const [reqBody, setReqBody] = useState(msgDetails.reqBody);
  const [resHeader, setResHeader] = useState(msgDetails.resHeader);
  const [resBody, setResBody] = useState(msgDetails.resBody);
  const [remarks, setRemarks] = useState();
  const isBackBtnVisible = true;
  const isSaveBtnVisible = true;
  const isNextBtnVisible = false;

  const handleOnBack = () => {
    //Do nothing
    // Ensure this is passed from calling the component. Or handle gracefully
    hideMessage();
  };

  const handleOnSave = () => {
    //TODO: Save to db and go back
    hideMessage();
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
      {fuzzRequestURI && (
        <div className="fuzz-div">
          <div className="info-container">
            <label>
              <b>Modify Request</b>
            </label>
            <hr />
            <label>Form new URIs by replacing following nouns: {nouns}</label>
          </div>
          <div className="info-container">
            <label>URI 1</label>
          </div>
          <input
            className="fuzz-uri-input"
            disabled={!editable}
            value={uri}
            onChange={handleURIChange}
          />
          <div className="info-container">
            <label>URI 2</label>
          </div>
          <input
            className="fuzz-uri-input"
            disabled={!editable}
            value={uri}
            onChange={handleURIChange}
          />
          <div className="info-container">
            <label>Add Remarks(If any)</label>
          </div>
          <textarea
            className="remarks"
            disabled={!editable}
            value=""
            onChange={handleResBodyChange}
          />
        </div>
      )}
      {fuzzRequestPayload && (
        <div className="fuzz-div">
          <div className="info-container">
            <label>
              <b>Modify Request</b>
            </label>
            <hr />
            <label>
              Here are some attributes that can be used to fuzz request payload:{" "}
              {attributes}
            </label>
          </div>
          <div className="info-container">
            <label>Request 1</label>
          </div>
          <textarea
            className="fuzz-request-input"
            disabled={!editable}
            value={reqBody}
            onChange={handleReqBodyChange}
          />
          <div className="info-container">
            <label>Request 2</label>
          </div>
          <textarea
            className="fuzz-request-input"
            disabled={!editable}
            value={reqBody}
            onChange={handleReqBodyChange}
          />
          <div className="info-container">
            <label>Add Remarks(If any)</label>
          </div>
          <textarea
            className="remarks"
            disabled={!editable}
            value=""
            onChange={handleResBodyChange}
          />
        </div>
      )}
      {reviewRequest && (
        <div className="fuzz-div">
          <div className="info-container">
            <label>
              <b>Review Request</b>
            </label>
            <hr />
            <label>
              Look for unused attributes and unbind them from API response.
              Don't rely on client side filtering to hide them.
            </label>
          </div>
          <div className="info-container">
            <label>Add Remarks(If any)</label>
          </div>
          <textarea
            className="remarks"
            disabled={!editable}
            value=""
            onChange={handleResBodyChange}
          />
        </div>
      )}
      <div className="bottombarwrapper">
        <TestBottombar
          isBackBtnVisible={isBackBtnVisible}
          onBackHandle={handleOnBack}
          isSaveBtnVisible={isSaveBtnVisible}
          onSaveHandle={handleOnSave}
          isNextBtnVisible={isNextBtnVisible}
          onNextHandle={handleOnSave}
        />
      </div>
    </div>
  );
}
