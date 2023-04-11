import { useEffect, useState } from 'react'
import DataTable, { TableColumn } from 'react-data-table-component';


interface latestData {
  data: apiResult[]
  loading: boolean
}

interface apiResult {
  date_range: {
    start_date: string,
    end_date: string
  },
  cardboard: number,
  plastic: number,
  paper: number,
  metal: number,
  glass: number
}

const fetchTodaysData = (
  setLatestData: React.Dispatch<React.SetStateAction<latestData>>
) => {
  const body = JSON.stringify({
    "time_frame": "weeks",
    "duration": 10
  })
  fetch("https://99gixr5c5g.execute-api.us-east-2.amazonaws.com/objects/greencount_get_api", {
    method: 'POST',
    body,
  }).then(response => response.json())
  .then(result => {
    setLatestData({
      data: result,
      loading: false
    })
  })
  .catch(error => console.error(error))
}

const columns: TableColumn<apiResult>[] = [
  {
    name: 'Week',
    selector: row => row.date_range.start_date,
    sortable: true
  },
  {
    name: 'cardboard',
    selector: row => row.cardboard,
    sortable: true
  },
  {
    name: 'Plastic',
    selector: row => row.plastic,
    sortable: true
  },
  {
    name: 'Paper',
    selector: row => row.paper,
    sortable: true
  },
  {
    name: 'Metal',
    selector: row => row.metal,
    sortable: true
  },
  {
    name: 'Glass',
    selector: row => row.glass,
    sortable: true
  }
]

export const ReactDataTable = () => {
  const [latestData, setLatestData] = useState<latestData>({data: [], loading: true})

  useEffect(() => {
    fetchTodaysData(setLatestData)
  }, [])

  return (
    <div className='sm:basis-full basis-1/2 pt-5 flex-col'>
      <div className="flex-row">
        <div className="flex justify-center mb-3">
          <h1 className='text-2xl text-center rounded text-white p-2 box-decoration-slice bg-gradient-to-r from-purple to-pink'>Weekly Results</h1>
        </div>
      </div>
      <div className='flex-1'>
        <div className="flex flex-col w-[95%] mx-[2.5%] p-5 rounded-md bg-white/50">
          <table className="table-auto">
          { latestData.loading ? (
            <div className="bg-purple w-32 m-auto rounded px-3 py-2 text-white">
              Loading...
            </div>
          ):(
            <DataTable 
              title="Result"
              columns={columns}
              data={latestData.data}
              defaultSortFieldId="week"
              pagination
            />
          )
          }
          </table>
        </div>
      </div>
    </div>
  )
}