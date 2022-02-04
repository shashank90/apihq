import React, { useState } from "react";
import apiStyles from "./apiSelectorModal.module.css";
import buttons from "../common/buttons.module.css";
import Buttons from "../common/Buttons";
import { useHistory } from "react-router";
import { DeleteOutline } from "@material-ui/icons";

export default function APIDropdownModal(props) {
  const [apis, setApis] = React.useState(props.apis);
  const [selected, setSelected] = useState("Select URL");

  const values = [
    "Select URL",
    "/users/v1/api",
    "/orgs/v1/api",
    "/customer/v1/api '/",
  ];

  const isBackBtnVisible = true;
  const isActionBtnVisible = true;
  const isNextBtnVisible = false;
  const actionButtonLabel = "Scan";

  const history = useHistory();

  const handleOnBack = () => {
    history.push("/apis/scan");
  };

  const handleOnAction = () => {
    console.log("Inside handle on action");
    history.push("/apis/scan");
  };

  const inputArr = [];

  const [headerPairs, setHeaderPairs] = useState(inputArr);

  function handleApiPathChange(event) {
    setSelected(event.target.value);
    props.setApiPath(event.target.value);
  }

  const addHeaderPair = (e) => {
    e.preventDefault();
    setHeaderPairs((s) => {
      return [
        ...s,
        {
          type: "text",
          value: {},
        },
      ];
    });
  };

  const removeHeaderPair = (e) => {
    e.preventDefault();

    const index = e.target.id;
    setHeaderPairs((s) => {
      const newArr = s.slice();
      // Remove header pair
      if (index > -1) {
        newArr.splice(index, 1);
      }
      return newArr;
    });
  };

  const handleHeaderNameChange = (e) => {
    e.preventDefault();

    const index = e.target.id;
    setHeaderPairs((s) => {
      // Get copy of existing header pair
      const new_header_pair = { ...s[index].value };
      new_header_pair["headerName"] = e.target.value;
      // Create copy of existing array
      const newArr = s.slice();
      // Assign new value to new array(copied)
      newArr[index].value = new_header_pair;

      return newArr;
    });
  };

  const handleHeaderValueChange = (e) => {
    e.preventDefault();

    const index = e.target.id;
    setHeaderPairs((s) => {
      // Get copy of existing header pair
      const new_header_pair = { ...s[index].value };
      new_header_pair["headerValue"] = e.target.value;
      // Create copy of existing array
      const newArr = s.slice();
      // Assign new value to new array(copied)
      newArr[index].value = new_header_pair;

      return newArr;
    });
  };

  return (
    <form className={apiStyles.modal}>
      <h3>API Scan</h3>
      <div>
        <label htmlFor="url_selector">API Endpoint URL: </label>
        <select
          className={apiStyles.url_value}
          id="url_selector"
          value={selected}
          onChange={handleApiPathChange}
          inputProps={{
            name: "URL",
            id: "url",
          }}
        >
          {values.map((value, index) => {
            return <option value={value}>{value}</option>;
          })}
        </select>
      </div>
      <div className={apiStyles.header}>
        <div className={apiStyles.header_btn}>
          <button onClick={addHeaderPair} className={buttons.green_btn}>
            Add Authorization Headers
          </button>
        </div>
        <div className={apiStyles.header_pair}>
          {headerPairs.map((item, i) => {
            return (
              <div className={apiStyles.header_pair}>
                <div>
                  <label htmlFor={i} className={apiStyles.header_name_label}>
                    Header name:
                  </label>
                  <input
                    className={apiStyles.header_value}
                    onChange={handleHeaderNameChange}
                    value={item.value["headerName"]}
                    id={i}
                    type={item.type}
                    size="55"
                    required
                  />
                  <DeleteOutline
                    className="TargetListDelete"
                    onClick={removeHeaderPair}
                  />
                </div>
                <div>
                  <label htmlFor={i} className={apiStyles.header_label}>
                    Header value:
                  </label>
                  <input
                    className={apiStyles.header_value}
                    onChange={handleHeaderValueChange}
                    value={item.value["headerValue"]}
                    id={i}
                    type={item.type}
                    size="55"
                    required
                  />
                </div>
              </div>
            );
          })}
        </div>
      </div>
      <div>
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
    </form>
  );
}
