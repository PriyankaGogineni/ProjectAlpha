import { ReactDataTable } from "./components/DataTable";
import { TodaysData } from "./components/TodaysData";
import { YesterdaysData } from "./components/YesterdaysData";

function App() {

  return (
    <div className='min-h-screen flex flex-col pb-20 bg-gradient-to-r from-green to-blue'>
      {/* Latest Result */}
      <div className="flex flex-row">
        <TodaysData />

        <YesterdaysData />
      </div>

      <ReactDataTable />
    </div> 
  )
}

export default App
