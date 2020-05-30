import React from 'react';
import Loader from 'react-loader-spinner';
import './loadingScreen.css'

const LoadingScreen =()=> {
    return(
        <div className ="LoaderBody"  >
      <Loader type="ThreeDots" color="#2BAD60" height="100" width="100" />
    </div>
    );

}

export default LoadingScreen;