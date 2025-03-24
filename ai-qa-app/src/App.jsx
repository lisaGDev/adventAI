import React, { useState, useEffect } from "react";
import axios from "axios"; // For making HTTP requests to the backend

const App = () => {
    // State for storing the uploaded file
    const [file, setFile] = useState(null);
    // State for the user's question
    const [question, setQuestion] = useState("");
    // State for the AI-generated answer
    const [answer, setAnswer] = useState("");
    // State to track loading status
    const [loading, setLoading] = useState(false);
    // State to store list of uploaded books
    const [books, setBooks] = useState([]);
    // State to track the selected book ID
    const [selectedBook, setSelectedBook] = useState(null);

    // Fetch books from the backend when the component loads
    useEffect(() => {
        fetchBooks();
    }, []);

    // Function to fetch uploaded books from the backend
    const fetchBooks = async () => {
        try {
            const res = await axios.get("http://localhost:8000/books"); // Replace with actual backend endpoint
            setBooks(res.data); // Save books to state
        } catch (err) {
            console.error("Error fetching books:", err);
        }
    };

    // Handles the PDF file upload to the backend
    const handleUpload = async () => {
        if (!file) return alert("Please select a PDF to upload."); // Basic validation

        const formData = new FormData();
        formData.append("file", file); // Appends the PDF file to FormData

        try {
            setLoading(true); // Show loading spinner/message
            await axios.post("http://localhost:8000/upload", formData); // Send file to backend
            alert("Upload successful!"); // Show success message
            fetchBooks();
        } catch (err) {
            console.error(err);
            alert("Upload failed."); // Show error message
        } finally {
            setLoading(false); // Hide loading spinner/message
        }
    };

    // Sends a question to the backend and retrieves an answer
    const handleAsk = async () => {
        if (!question) return; // Don't send empty questions

        try {
            setLoading(true);
            const res = await axios.post("http://localhost:8000/ask", { question }); 
            setAnswer(res.data.answer); // Store the answer in state
        } 
        catch (err) {
            console.error(err);
            alert("Error getting answer."); // Handle error
        } finally {
            setLoading(false);
        }
    };

    // The UI rendering part
    return (
        <div className="min-h-screen bg-gray-100 p-6 flex flex-col items-center">
            {/* Main container with max width and padding */}
            <div className="max-w-2xl w-full bg-white p-6 rounded-2xl shadow-md space-y-6">
            <h1 className="text-2xl font-bold text-center">📚 AI Q&A from PDFs</h1>

            {/* PDF Upload Section */}
            <div>
                <label className="block font-medium mb-1">Upload PDF</label>
                <input
                    type="file"
                    accept=".pdf" // Only accept PDF files
                    onChange={(e) => setFile(e.target.files[0])} // Update state with selected file
                    className="w-full"
                />
                <button
                    onClick={handleUpload} // Trigger upload
                    className="mt-2 px-4 py-2 bg-blue-600 text-white rounded-xl hover:bg-blue-700"
                >
                Upload PDF
                </button>
            </div>

            {/* Question Input Section */}
            <div>
                <label className="block font-medium mb-1">Ask a Question</label>
                <input
                    type="text"
                    value={question} // Controlled input bound to state
                    onChange={(e) => setQuestion(e.target.value)} // Update state as user types
                    placeholder="What is chapter 3 about?"
                    className="w-full p-2 border border-gray-300 rounded-lg"
                />
                <button
                    onClick={handleAsk} // Trigger question submission
                    className="mt-2 px-4 py-2 bg-green-600 text-white rounded-xl hover:bg-green-700"
                >
                Ask
                </button>
            </div>

            {/* Loading state */}
            {loading && <p className="text-center text-gray-600">Loading...</p>}

            {/* Display answer if available */}
            {answer && (
                <div className="p-4 border border-green-200 bg-green-50 rounded-lg">
                <p className="font-semibold">Answer:</p>
                <p>{answer}</p>
                </div>
            )}
            </div>
        </div>
    );
};

// Export the component so it can be used in other files
export default App; 