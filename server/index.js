const express = require("express");
const app = express();
const mysql = require("mysql");
const cors = require("cors");
const PORT = 3301;

app.use(cors());
app.use(express.json());

const db = mysql.createConnection({
    user: "root",
    host: "localhost",
    password: "password",
    database: "passwordmanager",
});

app.post("/addpassword", (req, res) => {
    const { password, title } = req.body;
    db.query(
        "INSERT INTO passwords (password, title) VALUES (?,?)",
        [password, title],
        (err, result) => {
            if (err)
                console.log(err);
            else
                res.send("Success");
        }
    );
});

app.post("/addaccount", (req, res) => { //wip idk how to adjust master_email atm
  const { master_email, title, username, password, email, url, notes } = req.body;
  db.query(
      "INSERT INTO Master_acc (master_email, title, username, password, email, url, notes) VALUES (?,?,?,?,?,?,?)",
      [master_email, title, username, password, email, url, notes],
      (err, result) => {
          if (err)
              console.log(err);
          else
              res.send("Success");
      }
  );
});

app.listen(PORT, () => {
    console.log("Server is running");
});
