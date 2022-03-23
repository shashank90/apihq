import { Tab, Tabs, TabList, TabPanel } from "react-tabs";

export default function Tab(props) {
  function handleSelect(index, last) {
    console.log("Selected tab: " + index + ", Last tab: " + last);
  }

  setMsgDetails({});

  return (
    <div className="tabmenu">
      <Tabs onSelect={handleSelect} selectedIndex={2}>
        <TabList>
          {props.tabTitles.map((title) => {
            <Tab>{title}</Tab>;
          })}
        </TabList>

        {props.tabPanels.map((tabPanel) => {
          <TabPanel>{tabPanel.headers}</TabPanel>;
        })}
      </Tabs>
    </div>
  );
}
