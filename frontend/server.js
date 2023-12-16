const express = require('express');
const cors = require('cors');
const app = express();

// Enable CORS for all routes
app.use(cors());

// Define your routes and other configurations here...

const PORT = 5003;
app.listen(PORT, () => {
  console.log(`Server is running on http://127.0.0.3:${PORT}`);
});
