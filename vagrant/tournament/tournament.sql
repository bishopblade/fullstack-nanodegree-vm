-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE TABLE players (
    id serial PRIMARY KEY,
    name varchar(255)
);

CREATE TABLE matches (
    id serial PRIMARY KEY,
    winner integer REFERENCES players (id),
    loser integer REFERENCES players (id)
);

CREATE VIEW player_wins AS
SELECT players.*, count(matches.winner) AS wins
FROM players LEFT JOIN matches ON (players.id = matches.winner)
GROUP BY players.id;

CREATE VIEW player_losses AS
SELECT players.*, count(matches.loser) AS losses
FROM players LEFT JOIN matches ON (players.id = matches.loser)
GROUP BY players.id;

CREATE VIEW standings AS
SELECT player_wins.*, player_wins.wins + player_losses.losses AS matches
FROM player_wins JOIN player_losses ON (player_wins.id = player_losses.id)
ORDER BY wins DESC;
