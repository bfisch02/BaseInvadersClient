# MineHunters Client

### Background

In a distant time in a place far, far away, a competition rages amongst the space pilots. You own one of the ships, but you are not one of the pilots. You have something better up your sleeve: you have outfitted your ship with a computer which will execute any program you upload. It is now your job to write a program that will steer your ship to victory.

### Game Rules

The rules of the game are simple: there are preplaced markers in space, called mines. If your ship gets in range of one of the mines, the mine belongs to you until another ship gets in range. If more than one ship is in range, nobody owns the mine until only one ship is in range again. Each ship is equipped with a scanner that can detect the exact location and owner of all mines within a certain radius. Your ship gets points every second that you own a mine. After a predetermined time, the game ends and the ship with the most points wins.

### Instructions

Your job is to implement the getDirection() function in ship_logic.py, which controls your ship's angle. The getDirection() function takes in three arguments:
- username: This is your ship's name.
- position: This is your ship's current position, in the form [x, y].
- mines: This is a list of all mines your ship has detected over the course of the game. Each mine is a dictionary formatted as follows:
```
{
    point: [x, y],
    owner: owner
}
```

The "owner" of a mine is the username of the ship that owned the mine whenever it was most recently in range of your ship, or "--" if the mine was unowned.

The game board is 10,000 x 10,000, and the top-left corner represents point [0, 0]. Therefore, all x and y coordinates will fall between 0 and 9,999, inclusive. The edges of the game board do not act as walls, so your ship may wrap around from one end of the board to the other (think pac-man... unless that's before your time).

The getDirection() function should return the direction (in degrees) in which your ship should fly. The ship asks for a new direction twice per second by calling the getDirection() function. Think of getDirection() as the brains behind the whole operation: your ship provides the function with all the information it knows about the current state of the game, and your function uses this information to decide where your ship should go next.

### Helper Functions

The following functions are available for use by your getDirection() function:
- getDistance(p1, p2)
  - Arguments: Two points of the form [x, y]
  - Return value: The distance between p1 and p2.
- getAngle(p1, p2)
  - Arguments: Two points of the form [x, y]
  - Return value: The angle from p1 to p2 (in degrees).
