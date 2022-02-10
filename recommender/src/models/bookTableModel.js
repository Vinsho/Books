import "./bookTableModel.css"
import React from "react";

const BookTableModel = (books) => {
  let bookTable = [];
  let booksData = books.books;

  for (let i = 0; i < booksData.length; i++) {
    bookTable.push(
        <tr key={i}>
          <td className="Book-td">{booksData[i].author}</td>
          <td className="Book-td">{booksData[i].title}</td>
        </tr>
    )
  }
  if(booksData.length == 0){
      return <header className="Title-header">No recommendation found!</header>
  }
  return (
      <table className="Book-table">
        <tbody>
          <tr>
            <th className="Book-th">Author</th>
            <th className="Book-th">Title</th>
          </tr>
          {bookTable}
        </tbody>
      </table>
  )
}

export default BookTableModel