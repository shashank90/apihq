import "./issueDetails.css";
import Buttons from "../../components/common/Buttons";
export default function IssueDetails(props) {
  console.log("Inside Vuln Details");
  const vulnObj = props.vulnObject;
  console.log(vulnObj);

  const isBackBtnVisible = true;
  const isActionBtnVisible = true;
  const isNextBtnVisible = false;
  const actionButtonLabel = "Show Request";

  const alert = vulnObj.alert;
  const wascId = vulnObj.wascid;
  const cweId = vulnObj.cweid;
  const desc = vulnObj.desc;
  const confidence = vulnObj.confidence;
  const riskDesc = vulnObj.riskdesc;
  const instanceCount = vulnObj.count;
  const instances = JSON.stringify(vulnObj.instances);
  const solution = vulnObj.solution;
  const reference = vulnObj.reference;

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
        <label className="vulnDetailItemHeader">Alert:</label>
        <span className="vulnDetailItemValue">{alert}</span>
      </div>
      <div className="vulnDetailLargeItem">
        <label className="vulnDetailItemHeader">Description</label>
        <textarea value={desc} className="textAreaStyle" />
      </div>
      <div className="vulnDetailItem">
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
      </div>
    </div>
  );
}
