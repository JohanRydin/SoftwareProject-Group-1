

function randString(list)
{
    const randomIndex = Math.floor(Math.random() * list.length);
    return list[randomIndex];
}

export function SelectRows(gamePrefs, genrePrefs, wishList)
{
    var commands = []
    var titles = []

    if (length(gamePrefs) > 0)
    {
        const game = randString(gamePrefs)
        commands = [...commands, {"similar_to_games" : game}]
        titles = [...titles, "Because you liked ".concat(game)]
    }
    if (length(genrePrefs) > 0)
    {
        const genre = randString(genrePrefs)
        commands = [...commands, {"similar_to_genre" : genre}]
        titles = [...titles, "Games from the ".concat(genre).concat(" genre")]
    }
}

export default SelectRows;