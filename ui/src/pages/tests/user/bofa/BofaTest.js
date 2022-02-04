import { DataGrid } from "@material-ui/data-grid";
import { useState } from "react";
import { useHistory } from "react-router";
import UserDropdownList from "../../../../components/common/UserDropdownList";
import TestBottombar from "../../../../layout/testbottombar/TestBottombar";
import {
  johnMessages,
  messages,
  shashankMessages,
} from "../../../../store/dummyData";
import "../../../proxyTraffic/msgList.css";
import "./bofaTest.css";

export default function BofaTest() {
  const [user, setUser] = useState();
  const [data, setData] = useState(messages);
  const isBackBtnVisible = true;
  const isSaveBtnVisible = true;
  const isNextBtnVisible = true;
  const history = useHistory();

  const handleOnBack = () => {
    //Do nothing
    history.push("/tests/user");
  };

  const handleOnSave = () => {
    //TODO: Save to db and go back
    history.push("/tests/over-exposure");
  };

  function setUserName(userName) {
    setUser(userName);
    console.log("Set username " + userName);
    if (userName == "Unauthenticated") {
      setData(messages);
    }
    if (userName == "John") {
      setData(shashankMessages);
    }
    if (userName == "Shashank") {
      setData(johnMessages);
    }
  }

  //useEffect(() => {}, []);
  // const data = contextData.getMessages();

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
    <div className="bofa-test-container">
      <div className="bofa-description">
        <p>
          <h2>Broken Function Level Authorization</h2>
        </p>
        <p>
          <div>
            <h4>Description</h4>
          </div>
        </p>
        <p>
          The API relies on the client to use user level or admin level APIs as
          appropriate. Attackers figure out the “hidden” admin API methods and
          invoke them directly.
        </p>
        <p>
          <h4>Process</h4>
        </p>
        <p>
          <ol>
            <li>Login as 2 users. One normal and other a privileged one.</li>
            <li>Select a user from below dropdown.</li>
            <li>
              For selected user, multi-select URIs that should be tested for
              access denial.
            </li>
          </ol>
        </p>
      </div>
      <div className="bofa-msgList">
        <UserDropdownList setUserName={setUserName} />
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
