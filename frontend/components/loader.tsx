import React from 'react'
import PropagateLoader  from "react-spinners/PropagateLoader";

const Loader = () => {
  return (
    <PropagateLoader
        className='animate-pulse bg-blue-500 mt-4'
        size={10}
        aria-label="Loading Spinner"
    />
  )
}

export default Loader