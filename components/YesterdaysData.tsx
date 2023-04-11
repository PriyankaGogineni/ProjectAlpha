import { useEffect, useState } from 'react'

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
  paper: number
  metal: number
  glass: number
}

const fetchTodaysData = (
  setLatestData: React.Dispatch<React.SetStateAction<latestData>>
) => {
  const body = JSON.stringify({
    "time_frame": "days",
    "duration": 2
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

export const YesterdaysData = () => {
  const [latestData, setLatestData] = useState<latestData>({data: [], loading: true})

  useEffect(() => {
    fetchTodaysData(setLatestData)
  }, [])

  return (
    <div className='sm:flex-1 basis-1/2 pt-5 flex-col'>
      <div className="flex-row">
        <div className="flex justify-center mb-3">
          <h1 className='text-2xl text-center rounded text-white p-2 box-decoration-slice bg-gradient-to-r from-purple to-pink'>Yesterday's Results</h1>
        </div>
      </div>
      <div className='flex-1'>
        <div className="flex flex-col w-[90%] mx-[5%] p-5 rounded-md bg-white/50">
          <table className="table-auto">
          { latestData.loading ? (
            <div className="bg-purple w-32 m-auto rounded px-3 py-2 text-white">
              Loading...
            </div>
          ):(
            <tbody>
              <tr>
                <td className='pb-5'>Date</td>
                <td>{latestData.data[0].date_range.start_date}</td>
              </tr>
              <tr>
                <td>No of Cardboard</td>
                <td>{latestData.data[0].cardboard}</td>
              </tr>
              <tr>
                <td>No. of Plastic</td>
                <td>{latestData.data[0].plastic}</td>
              </tr>
              <tr>
                <td>No. of Paper</td>
                <td>{latestData.data[0].paper}</td>
              </tr>
              <tr>
                <td>No. of Metal</td>
                <td>{latestData.data[0].metal}</td>
              </tr>
              <tr>
                <td>No. of Glass</td>
                <td>{latestData.data[0].glass}</td>
              </tr>
            </tbody>
          )
          }
          </table>
        </div>
      </div>
    </div>
  )
}