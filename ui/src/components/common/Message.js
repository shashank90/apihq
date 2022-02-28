import { useState } from "react";
import styles from "./msgDetails.module.css";
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
    <div className={styles.msgWrapper}>
      <div className={styles.buttonWrapper}>
        <Buttons
          isBackBtnVisible={isBackBtnVisible}
          onBackHandle={handleOnBack}
        />
      </div>
      <div className={styles.requestHeaderWrapper}>
        <h2>Request Details</h2>
      </div>
      <div className={styles.msgGridWrapper}>
        <div className={styles.requestUriLabel}>
          <label>URI</label>
        </div>
        <input
          className={styles.requestUri}
          disabled={!editable}
          value={uri}
          onChange={handleURIChange}
        />
        <div className={styles.requestHeaderLabel}>
          <label>Request Header</label>
        </div>
        <textarea
          className={styles.requestHeader}
          disabled={!editable}
          value={reqHeader}
          onChange={handleReqHeaderChange}
        />
        <div className={styles.requestBodyLabel}>
          <label>Request Body</label>
        </div>
        <textarea
          className={styles.requestBody}
          disabled={!editable}
          value={reqBody}
          onChange={handleReqBodyChange}
        />
        <div className={styles.responseHeaderLabel}>
          <label>Response Header</label>
        </div>
        <textarea
          className={styles.responseHeader}
          disabled={!editable}
          value={resHeader}
          onChange={handleResHeaderChange}
        />
        <div className={styles.responseBodyLabel}>
          <label>Response Body</label>
        </div>
        <textarea
          className={styles.responseBody}
          disabled={!editable}
          value={resBody}
          onChange={handleResBodyChange}
        />
      </div>
    </div>
  );
}
