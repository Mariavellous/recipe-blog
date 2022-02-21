import logo from './logo.svg';
import './App.css';
import {get} from 'axios'
import React from "react";
import {BrowserRouter, Link} from "react-router-dom";

import {data} from './post-data'


function App() {
    // console.log(data)
    // Make a request
    // get('http://0.0.0.0:5002/api')
    //     .then(function (response) {
    //       console.log(response);

//      let createRecipe = (data) => {
//         return <[post-data] all_recipes={data} key={data.title}/>
// }
    let my_func = (entry) => {
        return <div key={entry.id}>
            <div>{entry.title}</div>
            <div>{entry.date}</div>
            <Link to="/recipe">Recipe</Link>
        </div>
    }
    let entries = data.map(my_func)


    return <div className="All_Recipes">
        {entries}
    </div>
    //
    //
    // return (
    //     <div className="App">
    //         <header className="App-header">
    //             <img src={logo} className="App-logo" alt="logo"/>
    //             <p>
    //                 Edit <code>src/App.js</code> and save to reload.
    //             </p>
    //             <a
    //                 className="App-link"
    //                 href="https://reactjs.org"
    //                 target="_blank"
    //                 rel="noopener noreferrer"
    //             >
    //                 Learn React
    //             </a>
    //         </header>
    //     </div>
    // );
}

export default App;
