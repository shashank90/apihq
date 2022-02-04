import { DataGrid } from "@material-ui/data-grid";
import { useState } from "react";
import { useHistory } from "react-router";
import TestBottombar from "../../../../layout/testbottombar/TestBottombar";
import UserDropdownList from "../../../../components/common/UserDropdownList";
import {
  johnMessages,
  shashankMessages,
  messages,
} from "../../../../store/dummyData";
import "../../../proxyTraffic/msgList.css";
import "./resLimitTest.css";

export default function ResourceLimitTest() {
  const [test, setTest] = useState();
  const [data, setData] = useState(messages);
  const isBackBtnVisible = true;
  const isSaveBtnVisible = true;
  const isNextBtnVisible = true;
  const history = useHistory();

  //let data = messages;

  const handleOnBack = () => {
    //Do nothing
    history.push("/tests/user");
  };

  const handleOnSave = () => {
    //TODO: Save to db and go back
    history.push("/tests/sensitive-data");
  };

  function setTestName(test) {
    setTest(test);
    console.log("Set test " + test);
    if (test == "Rate Limit") {
      setData(messages);
    }
    if (test == "Zip Bomb") {
      setData(shashankMessages);
    }
  }

  const columns = [
    { field: "id", headerName: "ID", width: 90 },
    {
      field: "URI",
      headerName: "URI",
      width: 400,
      renderCell: (params) => {
        return <div className="msgListItem">{params.row.request.uri}</div>;
      },
    },
    {
      field: "Status Code",
      headerName: "Status Code",
      width: 200,
      renderCell: (params) => {
        return (
          <div className="msgListItem">{params.row.response.statusCode}</div>
        );
      },
    },
  ];

  return (
    <div className="res-test-container">
      <div className="res-description">
        <p>
          <h2>Resources and Rate-limiting review</h2>
        </p>
        <p>
          <h4>Description</h4>
        </p>
        <p>
          The API is not protected against an excessive amount of calls or
          payload sizes. Attackers can use this for Denial of Service (DoS) and
          authentication flaws like brute force attacks. Bombing the API with
          too many requests or too big payloads can make the API crash, possibly
          with unexpected results.
        </p>
        <h4>Process</h4>
      </div>
      <div className="res-msgList">
        <h5>
          1. Select APIs for a Rate-limit test. These APIs will be bombarded
          with bursty traffic
        </h5>
        <DataGrid
          rows={data}
          disableSelectionOnClick
          columns={columns}
          pageSize={4}
          checkboxSelection
        />
      </div>
      <div className="res-msgList">
        <h5>
          2. Select APIs for a Zip bomb test. These APIs will be uploaded with a
          highly dense and deeply nested zip file
        </h5>
        <DataGrid
          rows={data}
          disableSelectionOnClick
          columns={columns}
          pageSize={4}
          checkboxSelection
        />
      </div>
      <TestBottombar
        isBackBtnVisible={isBackBtnVisible}
        onBackHandle={handleOnBack}
        isSaveBtnVisible={isSaveBtnVisible}
        onSaveHandle={handleOnSave}
        isNextBtnVisible={isNextBtnVisible}
        onNextHandle={handleOnSave}
      />
    </div>
  );
}
