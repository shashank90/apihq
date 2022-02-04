import "./newTarget.css";
import { Link } from "react-router-dom";
import { useState } from "react";
import Checkbox from "../../components/common/Checkbox";

export default function NewTarget() {
  const [checkedItems, setCheckedItems] = useState({});
  const checkboxes = [
    {
      id: 1,
      name: "builtInTests",
      label: "Built-in Tests",
    },
    {
      id: 2,
      name: "userTests",
      label: "User Tests",
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
    <div className="newTarget">
      <h1 className="addTargetTitle">New Target Profile</h1>
      <form className="addTargetForm">
        <h3>Target Details</h3>
        <hr />
        <div className="addTargetItem">
          <label>Site</label>
          <input type="text" placeholder="www.example.com" />
        </div>
        <div className="addTargetItem">
          <label>Target Reconnaissance File</label>
          <input type="file" id="target_recon_file" />
        </div>
        <h3>Authentication Details</h3>
        <hr />
        <div className="addTargetItem">
          <label>Username</label>
          <input type="text" placeholder="" />
        </div>
        <div className="addTargetItem">
          <label>Password</label>
          {/* <select name="active" id="active">
            <option value="yes">Yes</option>
            <option value="no">No</option>
          </select> */}
          <input type="password" placeholder="" />
        </div>
        <div className="addTargetItem">
          <label>Additional Input</label>
          <input
            type="text"
            placeholder="{'loginURI':'www.example.com/login?csrf-token=0826afe4-9d34-4718-90a1-2419171d4ac8'}"
          />
        </div>
        <div className="addTargetItem">
          <label>Authentication Script</label>
          <input type="file" id="auth_script" />
        </div>
        <h3>Scan Details</h3>
        <hr />
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
        <div className="btn-cluster">
          <Link to="/Targets">
            <button className="addTargetButton">Save</button>
          </Link>
          <Link to="/proxy/messages">
            <button className="addTargetButton">Save and Proxy</button>
          </Link>
        </div>
      </form>
    </div>
  );
}
