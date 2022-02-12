import "./issueDetails.css";
import Buttons from "../../components/common/Buttons";
export default function IssueDetails(props) {
  const detail = props.detail;
  console.log(detail);

  const isBackBtnVisible = true;
  const isActionBtnVisible = true;
  const isNextBtnVisible = false;
  const actionButtonLabel = "Show Request";

  const description = detail.description;
  // const wascId = detail.wascid;
  // const cweId = detail.cweid;
  const message = detail.message;
  console.log(message);
  // const confidence = detail.confidence;
  // const riskDesc = detail.riskdesc;
  // const instanceCount = detail.count;
  // const instances = JSON.stringify(detail.instances);
  // const solution = detail.solution;
  // const reference = detail.reference;

  const msgItems = message.map((d, index) => <li key={index}>{d}</li>);

  function handleOnAction() {}

  const handleOnBack = () => {
    props.setIssueSelected(false);
  };

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
        <label className="vulnDetailItemHeader" htmlFor="description">
          Description:
        </label>
        <span className="vulnDetailItemValue" id="description">
          {description}
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
      {/* <div className="vulnDetailItem">
        <label className="vulnDetailItemHeader">WASCID:</label>
        <span className="vulnDetailItemValue">{wascId}</span>
      </div>
      <div className="vulnDetailItem">
        <label className="vulnDetailItemHeader">CWEID:</label>
        <span className="vulnDetailItemValue">{cweId}</span>
      </div>
      <div className="vulnDetailItem">
        <label className="vulnDetailItemHeader">Confidence:</label>
        <span className="vulnDetailItemValue">{confidence}</span>
      </div>
      <div className="vulnDetailItem">
        <label className="vulnDetailItemHeader">Risk Level:</label>
        <span className="vulnDetailItemValue">{riskDesc}</span>
      </div>
      <div className="vulnDetailItem">
        <label className="vulnDetailItemHeader">Instance Count:</label>
        <span className="vulnDetailItemValue">{instanceCount}</span>
      </div>
      <div className="vulnDetailLargeItem">
        <label className="vulnDetailItemHeader">Instances</label>
        <textarea value={instances} className="textAreaStyle" />
      </div>
      <div className="vulnDetailLargeItem">
        <label className="vulnDetailItemHeader">Solution</label>
        <textarea value={solution} className="textAreaStyle" />
      </div>
      <div className="vulnDetailLargeItem">
        <label className="vulnDetailItemHeader">Reference</label>
        <textarea value={reference} className="textAreaStyle" />
      </div> */}
    </div>
  );
}
