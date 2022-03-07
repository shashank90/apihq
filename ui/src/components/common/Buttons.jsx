import React from "react";
import "./buttons.css";

export default function Buttons(props) {
  let isBackBtnVisible = false;
  const onBackHandle = props.onBackHandle;
  let isActionBtnVisible = false;
  const onActionHandle = props.onActionHandle;
  let isNextBtnVisible = false;
  const onNextHandle = props.onNextHandle;

  const actionButtonLabel = props.actionButtonLabel
  const actionButtonDisable = props.actionButtonDisable

  isBackBtnVisible = props.isBackBtnVisible;
  isActionBtnVisible = props.isActionBtnVisible;
  isNextBtnVisible = props.isNextBtnVisible;

  return (
    <div className="tbottombarWrapper">
      {isBackBtnVisible && (
        <button className="tback-btn" onClick={onBackHandle}>
          Back
        </button>
      )}
      <div className="tsave-next-wrapper">
        {isActionBtnVisible && (
          <button className="tsave-btn" onClick={onActionHandle}>
            {actionButtonLabel}
          </button>
        )}
        {isNextBtnVisible && (
          <button className="tnext-btn" onClick={onNextHandle}>
            Next
          </button>
        )}
      </div>
    </div>
  );
}
