const BASE_URL = 'http://localhost:8000';

const API_KEY = import.meta.env.VITE_API_KEY;

/**
 * Helper function to make GET requests
 * @param {string} path - The API endpoint path
 * @param {object} [params={}] - Query parameters to include in the request
 * @returns {Promise} - The response data or error
 */
const fetchData = async (path, params = {}) => {
  try {
    const queryString = new URLSearchParams(params).toString();
    const url = `${BASE_URL}${path}${queryString ? `?${queryString}` : ''}`;
    const response = await fetch(url, {mode:'cors'});

    if (!response.ok) {
      throw new Error(`Error fetching data from ${path}: ${response.statusText}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error(error);
    throw error;
  }
};

/**
 * Helper function to make POST requests
 * @param {string} path - The API endpoint path
 * @param {object} data - The payload to send in the request body
 * @param {object} [headers={}] - Additional headers (e.g., { 'Content-Type': 'application/json' })
 * @returns {Promise} - The response data or error
 */
const postData = async (path, data, headers = { 'Content-Type': 'application/json' }) => {
  try {
    console.log(`${BASE_URL}${path}`)
    console.log(JSON.stringify(data))
    const response = await fetch(`${BASE_URL}${path}`, {
      method: 'POST',
      headers,
      body: JSON.stringify(data),
      mode:'cors',
    });

    if (!response.ok) {
      throw new Error(`Error posting data to ${path}: ${response.statusText}`);
    }

    const responseData = await response.json();
    return responseData;
  } catch (error) {
    console.error(error);
    throw error;
  }
};

/**
 * Helper function to make PUT requests
 * @param {string} path - The API endpoint path (e.g., '/users/:id')
 * @param {object} data - The payload to send in the request body
 * @param {object} [headers={}] - Additional headers (e.g., { 'Content-Type': 'application/json' })
 * @returns {Promise} - The response data or error
 */
const putData = async (path, data, headers = { 'Content-Type': 'application/json' }) => {
  try {
    const response = await fetch(`${BASE_URL}${path}`, {
      method: 'PUT',
      headers,
      body: JSON.stringify(data),
      mode:'cors',
    });

    if (!response.ok) {
      throw new Error(`Error updating data at ${path}: ${response.statusText}`);
    }

    const responseData = await response.json();
    return responseData;
  } catch (error) {
    console.error(error);
    throw error;
  }
};

/**
 * Helper function to make DELETE requests
 * @param {string} path - The API endpoint path (e.g., '/users/:id')
 * @returns {Promise} - The response data or error
 */
const deleteData = async (path) => {
  try {
    const response = await fetch(`${BASE_URL}${path}`, { method: 'DELETE' , mode: 'cors'});

    if (!response.ok) {
      throw new Error(`Error deleting data at ${path}: ${response.statusText}`);
    }

    const responseData = await response.json();
    return responseData;
  } catch (error) {
    console.error(error);
    throw error;
  }
};

export const getUser = (userID) => {
    var data = {userID: userID}
    return fetchData("/user", data);
}

export const postUser = (username) => {
    var data = {username: username}
    return postData("/user", data);
}

// userID example: 5
// rows example:   [{"similar_to" : [1, 5, 2]}, {"best_reviewed" : "Action"}, {"similar_to" : "all"}, {"best_sales" : "Adventure"}]
export const getRecommendations = (userID, rows) => {
    var data = {userID: userID, rows: rows}
    return postData("/recommendation", data)
}

export const postGamePreference = (userID, gameID) => {
    var data =  {userID: userID, gameID: gameID}
    return postData("/gamePref", data)
}

export const postGenrePreference = (userID, genre) => {
  var data =  {userID: userID, genre: genre}
  return postData("/genrePref", data)
}

export const postWishlistGame = (userID, gameID) => {
  var data =  {userID: userID, gameID: gameID}
  return postData("/wishlist", data)
}

export const deleteGamePreference = (userID, gameID) => {
  var data =  {userID: userID, gameID: gameID}
  return deleteData("/gamePref", data)
}

export const deleteGenrePreference = (userID, genre) => {
  var data =  {userID: userID, genre: genre}
  return deleteData("/genrePref", data)
}

export const deleteWishlistGame = (userID, gameID) => {
  var data =  {userID: userID, gameID: gameID}
  return deleteData("/wishlist", data)
}

export const getSearch = (search) => {
  var data = {search: search}
  return fetchData("/search", data);
}

// Convert any string into a slug to be used in a url
// str - string to convert
// ex: stringToSlug("Cyberpunk 2077") -> "cyberpunk-2077"
function stringToSlug(str) {
  console.log(str)
  return str
    .toLowerCase()                      // Convert the string to lowercase
    .trim()                             // Remove whitespace from both ends
    .replace(/[^a-z0-9\s-]/g, '')       // Remove special characters
    .replace(/\s+/g, '-')               // Replace spaces with hyphens
    .replace(/-+/g, '-');               // Collapse consecutive hyphens
}

export const getGameImage = (gameName) => {
  const slug = stringToSlug(gameName)
  return fetch(`https://rawg.io/api/games/${slug}?key=${API_KEY}`, {mode: 'cors'})
          .then(res => res.json())
          .then(data => {return data.background_image})
          .catch(error => console.error('Error:', error));
}
