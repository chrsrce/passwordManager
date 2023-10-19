import "./App.css";
import { useState } from "react";
import Axios from "axios";



function App() {
    const [title, setTitle] = useState("");
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState(""); //initally "", use setPassword to trigger updated current password
    const [email, setEmail] = useState("");
    const [url, setUrl] = useState("");
    const [notes, setNotes] = useState("");

    const addPassword = () => {
        Axios.post("http://localhost:3001/addpassword", {
            password: password,
            title: title,
        });
    };

    const addAccount = () => {
        Axios.post("http://localhost:3001/addaccount", {
            title: title,
            username: username,
            password: password,
            email: email,
            url: url,
            notes: notes,
        });
    };

    return (
        <div className="App">
            <div className="AddingAccount">
                <label className="InputLabel" htmlFor="title">
                    Title
                </label>
                <input
                    type="text"
                    id="title"
                    placeholder=" "
                    onChange={(event) => {
                        setTitle(event.target.value);
                    }}
                />

                <label className="InputLabel" htmlFor="username">
                    Username
                </label>
                <input
                    type="text"
                    id="username"
                    placeholder=" "
                    onChange={(event) => {
                        setUsername(event.target.value);
                    }}
                />

                <label className="InputLabel" htmlFor="password">
                    Password
                </label>
                <input
                    type="text"
                    id="password"
                    placeholder=" "
                    onChange={(event) => {
                        setPassword(event.target.value);
                    }}
                />

                <label className="InputLabel" htmlFor="email">
                    Email
                </label>
                <input
                    type="text"
                    id="email"
                    placeholder=" "
                    onChange={(event) => {
                        setEmail(event.target.value);
                    }}
                />

                <label className="InputLabel" htmlFor="url">
                    URL
                </label>
                <input
                    type="text"
                    id="url"
                    placeholder=" "
                    onChange={(event) => {
                        setUrl(event.target.value);
                    }}
                />

                <label className="InputLabel" htmlFor="notes">
                    Notes
                </label>
                <input
                    type="long_text"
                    id="notes"
                    placeholder=" "
                    onChange={(event) => {
                        setNotes(event.target.value);
                    }}
                />

                <button onClick={addPassword}> Add Account</button>
            </div>
        </div>
    );
}

export default App;
