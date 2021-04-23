import './App.css';
import logo from './logo.png'
import NeighborChart from "./charts/neighbors/Neighbors";
import DailyChart from "./charts/daily/Daily";
import ApplianceChart from "./charts/appliances/Appliances";
import UserProfile from "./other/user-info/UserInfo";
import ApplianceInfo from "./other/app-info/ApplianceInfo";


function App() {

  return (
    <div className="App">
      <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
        <h3>
          My Energy
        </h3>
      </header>
        <div className="Content">
            <div id="side-content">
                <UserProfile />
                <ApplianceInfo />
            </div>
            <div id="main-content">
                <div className='Chart-Container' id='main-chart'>
                    <h3>Daily Energy Usage</h3>
                    <DailyChart />
                </div>
                <div className='Chart-Container' id="sub-charts">
                    <div className='Sub-Chart'>
                        <h3>Energy Usage by Appliance</h3>
                        <ApplianceChart />
                    </div>
                    <div className='Sub-Chart'>
                        <h3>Neighborhood Comparison</h3>
                        <NeighborChart />
                    </div>
                </div>
            </div>
        </div>
    </div>
  );
}



export default App;
