import "../../../proxyTraffic/msgList.css";
import "./sdTest.css";
import { useContext, useState } from "react";
import Checkbox from "../../../../components/common/Checkbox";
import Buttons from "../../../../components/common/Buttons";
import { Link, useHistory } from "react-router-dom";

export default function SdTest() {
  const history = useHistory();
  const isBackBtnVisible = true;
  const isSaveBtnVisible = true;
  const isNextBtnVisible = false;

  const handleOnBack = () => {
    //Do nothing
    history.push("/tests/user");
  };

  const handleOnSave = () => {
    //TODO: Save to db and go back
    history.push("/tests/user");
  };

  const [checkedItems, setCheckedItems] = useState({});
  const checkboxes = [
    {
      id: 1,
      name: "email",
      label: "Email",
    },
    {
      id: 2,
      name: "mobile",
      label: "Mobile",
    },
    {
      id: 3,
      name: "panNumber",
      label: "PAN Number",
    },
    {
      id: 4,
      name: "aadhar",
      label: "Aadhar",
    },
    {
      id: 5,
      name: "drivingLicense",
      label: "Driving License",
    },
  ];

  const handleChange = (event) => {
    setCheckedItems({
      ...checkedItems,
      [event.target.name]: event.target.checked,
    });
    console.log("checkedItems: ", checkedItems);
  };

  return (
    <div className="sd-test-container">
      <div className="sd-description">
        <p>
          <h2>Sensitive Data Exposure</h2>
        </p>
        <p>
          <h4>Description</h4>
        </p>
        <p>
          Lack of proper logging, monitoring, and alerting allows attacks and
          attackers go unnoticed.
        </p>
        <p>
          <h4>Process</h4>
        </p>
        <p>
          <ol>
            <li>
              Enter regex to check for sensitive data in API responses and log
            </li>
            <li>Upload log file to scan for sensitive data</li>
          </ol>
        </p>
      </div>
      <form className="sd-form">
        <div className="addTargetItem">
          <ul className="ul-no-bullets">
            {checkboxes.map((item) => (
              <li key={item.id}>
                <Checkbox
                  label={item.label}
                  name={item.name}
                  checked={checkedItems[item.name]}
                  onChange={handleChange}
                />
              </li>
            ))}
          </ul>
        </div>
        <div className="addTargetItem">
          <label>Regex 1</label>
          <input type="text" />
        </div>
        <div className="addTargetItem">
          <label>Regex 2</label>
          <input type="text" placeholder="" />
        </div>
        <div className="addTargetItem">
          <label>Regex 3</label>
          <input type="text" placeholder="" />
        </div>
        <div className="addTargetItem">
          <label>Log File</label>
          <input type="file" id="target_recon_file" />
        </div>
        <Buttons
          isBackBtnVisible={isBackBtnVisible}
          onBackHandle={handleOnBack}
          isSaveBtnVisible={isSaveBtnVisible}
          onSaveHandle={handleOnSave}
          isNextBtnVisible={isNextBtnVisible}
          onNextHandle={handleOnSave}
        />
      </form>
    </div>
  );
}
