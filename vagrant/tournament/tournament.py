#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection and cursor."""
    conn = psycopg2.connect("dbname=tournament")
    cursor = conn.cursor()

    return (conn, cursor)

def end(conn, cursor):
    """Commit changes to database and close cursor and connection."""
    conn.commit()
    cursor.close()
    conn.close()

def deleteMatches():
    """Remove all the match records from the database."""
    conn, cursor = connect()
    cursor.execute("TRUNCATE TABLE matches")
    end(conn, cursor)

def deletePlayers():
    """Remove all the player records from the database."""
    conn, cursor = connect()
    cursor.execute("TRUNCATE TABLE players CASCADE")
    end(conn, cursor)

def countPlayers():
    """Returns the number of players currently registered."""
    conn, cursor = connect()
    cursor.execute("SELECT count(*) FROM players")
    count = cursor.fetchone()[0]
    end(conn, cursor)

    return count

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn, cursor = connect()
    cursor.execute("INSERT INTO players (name) VALUES (%s)", (name,))
    end(conn, cursor)

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn, cursor = connect()
    cursor.execute("SELECT * FROM standings")
    standings = cursor.fetchall()
    end(conn, cursor)

    return standings

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn, cursor = connect()
    cursor.execute("INSERT INTO matches (winner, loser) VALUES (%s, %s)", (winner, loser))
    end(conn, cursor)
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    standings = playerStandings()
    matchups = []

    # Iterate through standings in pairs and match each pair of players together
    for i in range(0, len(standings) - 1, 2):
        first = standings[i]
        second = standings[i+1]
        matchups.append((first[0], first[1], second[0], second[1]))
    return matchups
