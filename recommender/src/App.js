import './App.css';
import React, {useState} from "react";
import BookTableModel from './models/bookTableModel'

function App() {
  const [books, setBooks] = useState([]);
  const [message, setMessage] = useState("");

  const fetchBooks = async() =>{
    let title = document.getElementById("bookTitle").value;
    let author = document.getElementById("bookAuthor").value;
    let parsedBooksData;

    const config = {
      method: "POST",
      body: JSON.stringify({"title": title, "author": author})
    }
    try{
      const booksData = await fetch(`http://127.0.0.1:5000/recommendation`,
          config);
      parsedBooksData = JSON.parse(await booksData.json());
    }
    catch(error){
      parsedBooksData = null;
    }
    setBooks(BookTableModel(parsedBooksData));
    if (parsedBooksData.found == false && parsedBooksData.books.length != 0){
      setMessage(<header className="Title-header">Title not found! Perhaps you meant:</header>)
    }
    else{
      setMessage("")
    }
  }

  return (
    <div className="App">
      <header className="App-header">Get a book recommendation!</header>
      <div className="Input-div">
        <header className="Title-header">Enter your favourite book here:</header>
        <input className="Title-input" type="text" id="bookTitle" placeholder="Book title"/><br/>
        <input className="Title-input" type="text" id="bookAuthor" placeholder="Book author"/><br/>
        <button onClick={fetchBooks} className="Title-button">
            Submit
        </button>
      </div>
      {message}
      {books}
    </div>
  );
}

export default App;
