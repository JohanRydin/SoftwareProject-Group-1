const ranking_genres = ['Action', 'Adventure', 'Role-Playing', 'Simulation', 'Strategy', 'Sports & Racing']

function randString(list)
{
    const randomIndex = Math.floor(Math.random() * list.length);
    return list[randomIndex];
}

/*  Get some commands for rows based on user preferences
    @note - Selects games randomly based on this information
    @param gamePrefs - The games that the user likes as list of gameobjects
    @param genrePrefes - The genres that the user likes as list of strings
    @param wishList - The wishlist of the user
    @returns [commands, titles] where commands is a list of dicts and titles a list of strings
*/
export function SelectRows(gamePrefs, genrePrefs, wishList)
{
    var commands = []
    var titles = []

    if (gamePrefs.length > 0)
    {
        const index = Math.floor(Math.random() * gamePrefs.length);
        const gameID = gamePrefs[index]['id']
        commands = [...commands, {"similar_to_games" : [gameID]}]
        titles = [...titles, "Because you liked ".concat(gamePrefs[index]['gamename'])]
    }
    if (genrePrefs.length > 0)
    {
        const genre = randString(genrePrefs)
        commands = [...commands, {"similar_to_genre" : genre}]
        titles = [...titles, "Games from the ".concat(genre).concat(" genre")]
    }
    if (genrePrefs.length > 0)
    {
        var filtered_genres = genrePrefs.filter(genre => ranking_genres.includes(genre))
        if (filtered_genres.length > 0)    // Only some genres contain ranking info in AIServer
        {
            const genre = randString(filtered_genres)
            commands = [...commands, {"best_reviewed" : genre}]
            titles = [...titles, "Best reviewed ".concat(genre).concat(" games")]
        }
    }
    if (genrePrefs.length > 0)
    {
        var filtered_genres = genrePrefs.filter(genre => ranking_genres.includes(genre))
        if (filtered_genres.length > 0)    // Only some genres contain ranking info in AIServer
        {
            const genre = randString(filtered_genres)
            commands = [...commands, {"best_sales" : genre}]
            titles = [...titles, "Most popular ".concat(genre).concat(" games")]
        }
    }

    return [commands, titles]
}

export default SelectRows;