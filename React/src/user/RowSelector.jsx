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
        commands = [...commands, {"similar_to_games" : "all"}]
        titles = [...titles, "Similar To What You Play"]
    }
    if (gamePrefs.length > 0)
    {
        const index = Math.floor(Math.random() * gamePrefs.length);
        const gameID = gamePrefs[index]['id']
        commands = [...commands, {"similar_to_games" : [gameID]}]
        titles = [...titles, "Because You Liked '".concat(gamePrefs[index]['gamename']).concat("'")]
    }
    if (genrePrefs.length > 0)
    {
        const genre = randString(genrePrefs)
        commands = [...commands, {"similar_to_genre" : genre}]
        titles = [...titles, "Games From The '".concat(genre).concat("' Genre")]
    }
    if (genrePrefs.length > 0)
    {
        var filtered_genres = genrePrefs.filter(genre => ranking_genres.includes(genre))
        if (filtered_genres.length > 0)    // Only some genres contain ranking info in AIServer
        {
            const genre = randString(filtered_genres)
            commands = [...commands, {"best_reviewed" : genre}]
            titles = [...titles, "Best Reviewed '".concat(genre).concat("' Games")]
        }
    }
    if (genrePrefs.length > 0)
    {
        var filtered_genres = genrePrefs.filter(genre => ranking_genres.includes(genre))
        if (filtered_genres.length > 0)    // Only some genres contain ranking info in AIServer
        {
            const genre = randString(filtered_genres)
            commands = [...commands, {"best_sales" : genre}]
            titles = [...titles, "Most Popular '".concat(genre).concat("' Games")]
        }
    }

    return [commands, titles]
}

export default SelectRows;
