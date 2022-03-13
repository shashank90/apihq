import "./issueDetails.css";
import { useState } from "react";
import Buttons from "../../components/common/Buttons";
import Message from "../../components/common/Message";
export default function IssueDetails(props) {
  const issueDetail = props.issueDetail.issue;
  // console.log(issueDetail);

  const isBackBtnVisible = true;
  const isActionBtnVisible = true;
  const isNextBtnVisible = false;
  const actionButtonLabel = "Show Request";
  const requestDetail = props.issueDetail.request;
  // console.log(requestDetail);
  const [showRequest, setShowRequest] = useState(false);

  // const wascId = detail.wascid;
  // const cweId = detail.cweid;
  const issueType = issueDetail.issueType;
  const message = issueDetail.message;
  const description = issueDetail.description;
  const solution = issueDetail.solution;
  // const confidence = detail.confidence;
  // const riskDesc = detail.riskdesc;
  // const instanceCount = detail.count;
  // const instances = JSON.stringify(detail.instances);
  // const solution = detail.solution;
  // const reference = detail.reference;

  const messageDetail = {
    url: requestDetail.request.url,
    reqHeader: requestDetail.request.header,
    reqBody: requestDetail.request.body,
    resHeader: requestDetail.response.header,
    resBody: requestDetail.response.body,
  };

  const msgItems = message.map((d, index) => <li key={index}>{d}</li>);

  function handleOnAction() {
    setShowRequest(true);
  }

  const handleOnBack = () => {
    props.setIssueSelected(false);
  };

  if (showRequest) {
    return <Message msgDetails={messageDetail} showRequest={setShowRequest} />;
  } else {
    return (
      <div className="vulnDetailsWrapper">
        <div className="btn-container">
          <Buttons
            isBackBtnVisible={isBackBtnVisible}
            onBackHandle={handleOnBack}
            isActionBtnVisible={isActionBtnVisible}
            onActionHandle={handleOnAction}
            actionButtonLabel={actionButtonLabel}
            isNextBtnVisible={isNextBtnVisible}
            onNextHandle={handleOnAction}
          />
        </div>
        <h2>Issue Details</h2>
        <div className="vulnDetailItem">
          <label className="vulnDetailItemHeader" htmlFor="issueType">
            Type:
          </label>
          <span className="vulnDetailItemValue" id="issueType">
            {issueType}
          </span>
        </div>
        <div className="vulnDetailLargeItem">
          <label className="vulnDetailItemHeader" htmlFor="msg">
            Message:
          </label>
          <div className="box" id="msg">
            {msgItems}
          </div>
        </div>
        <div className="vulnDetailLargeItem">
          <label className="vulnDetailItemHeader" htmlFor="description">
            Description:
          </label>
          <div className="box" id="description">
            {description}
          </div>
        </div>
        <div className="vulnDetailLargeItem">
          <label className="vulnDetailItemHeader" htmlFor="solution">
            Solution:
          </label>
          <div className="box" id="solution">
            {solution}
          </div>
        </div>
      </div>
    );
  }
}
