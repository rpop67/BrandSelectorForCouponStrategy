import React from 'react';
import Loader from 'react-loader-spinner';
import './loadingScreen.css'

const LoadingScreen =()=> {
    return(
        <div className ="LoaderBody"  >
      <Loader className="loadingSpinner" type="ThreeDots" color="#2BAD60" height="100" width="100" />
      <div><h3>Fetching and Analysing results . .</h3></div>
    </div>
    );

}

export default LoadingScreen;