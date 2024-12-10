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

export const getUser = (userName) => {
    return fetchData(`/user/${userName}`);
}

export const postUser = (username) => {
    var data = {username: username}
    return postData(`/users/`, data);
}


export const getGamePreferences = (userName) => {
  return fetchData(`/user/${userName}/gamePref`);
}

export const getGenrePreferences = (userName) => {
  return fetchData(`/user/${userName}/genrePref`);
}

export const getWishList = (userName) => {
  return fetchData(`/user/${userName}/wishlist`);
}


export const postGamePreference = (userName, gameID) => {
    var data = {gameID: gameID}
    return postData(`/user/${userName}/gamePref`, data)
}

export const postGenrePreference = (userName, genre) => {
  var data =  {genre: genre}
  return postData(`/user/${userName}/genrePref`, data)
}

export const postWishlistGame = (userName, gameID) => {
  var data =  {gameID: gameID}
  return postData(`/user/${userName}/wishlist`, data)
}


export const deleteGamePreference = (userName, gameID) => {
  var data =  {gameID: gameID}
  return deleteData(`/user/${userName}/gamePref/`, data)
}

export const deleteGenrePreference = (userName, genre) => {
  var data =  {genre: genre}
  return deleteData(`/user/${userName}/genrePref`, data)
}

export const deleteWishlistGame = (userName, gameID) => {
  var data =  {gameID: gameID}
  return deleteData(`/user/${userName}/wishlist`, data)
}


// username example: Erik
// rows example:   [{"similar_to" : [1, 5, 2]}, {"best_reviewed" : "Action"}, {"similar_to" : "all"}, {"best_sales" : "Adventure"}]
export const getRecommendations = (userName, rows) => {
  var data = {rows: rows}
  return postData(`/user/${userName}/recommendation`, data)
}

export const getSearch = (search) => {
  var data = {search: search}
  return fetchData(`/search`, data);
}


// Convert any string into a slug to be used in a url
// str - string to convert
// ex: stringToSlug("Cyberpunk 2077") -> "cyberpunk-2077"
function stringToSlug(str) {
  return str
    .toLowerCase()                      // Convert the string to lowercase
    .trim()                             // Remove whitespace from both ends
    .replace(/[^a-z0-9\s-]/g, '')       // Remove special characters
    .replace(/\s+/g, '-')               // Replace spaces with hyphens
    .replace(/-+/g, '-');               // Collapse consecutive hyphens
}

export const getGameImage = (gameName) => {
  const slug = stringToSlug(gameName)
  const defaultImage = 'https://img.freepik.com/premium-photo/vedio-games-illustration_1252102-47756.jpg?w=1480'; // Replace with your default image URL
  return fetch(`https://rawg.io/api/games/${slug}?key=${API_KEY}`, {mode: 'cors'})
          .then(res => res.json())
          .then((data) => {
            return data.background_image || defaultImage; // Use default image if background_image is missing
          })
          .catch((error) => {
            console.error('Error:', error);
            return defaultImage; // Use default image in case of an error
          });
}
