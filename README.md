# War Game

## How to Run
Execute the file named `war_game.py`. 

## The Game
* You, as the player, have to 
  * collect rewards.
  * dodge bomb and enemy bullets
  * Rescue civilians
  * Reach the base

* You as a commander
  * Change the parameters
  * Save parameters for repeated use
  * Keep track during the game through textual feedback and audio effects
  * Assess performance

## Entities

Entity | Movement | Ability / Properties
--- | --- | --- 
Soldier | <ul><li>Horizontal and Vertical</li><li>Step-wise</li></ul> | Throw bombs 
Enemy | <ul><li>Directionless</li><li>Cannot move during the game</li></ul> | <ul><li>Shoot</li><li>Point at player randomly</li></ul> 
Bombs | <ul><li>Angular</li><li>Uniform Speed</li></ul> | <ul><li>Explode</li><li>Damage done depends on distance from soldier</li></ul> 
Projectiles | <ul><li>Affected by gravity</li><li>Uniform Speed in x-direction</li></ul> | <ul><li>Thrown by players</li><li>Can hit and kill enemies</li></ul> 
Bonus (Target) | <ul><li>Cannot move during the gane</li><li>Can be placed freely anywhere</li></ul> | Collected by players
Civilians (Target) | <ul><li>Cannot move during the gane</li><li>Can be placed freely anywhere</li></ul> | Saved by players

## Files
* Entities
  * `enemy.py`, `soldier.py`, `bomb.py`, `civilian.py` and `bonus.py`
  * By changing the parameters of these classes and their methods, you can change things like
    * speed (for bullets, bomb or player)
    * algorithm used to calculate health damage

* `constants.py`
  * Defines constants used throughout the codebase (display width, height, colors, button sizes etc.)

* `sliders.py`
  * Defines appearance of the sliders on settings screen

* Buttons
  * `buttons.py`, `game_buttons.py`
  * Functions used to display buttons

* `load_image.py`
  * A function written to load image, given the file path and transform parameters (scale and angle).


## GIFs

<!-- ![](https://github.com/slowdivesun/war-game/blob/master/gifs/bomb_2.gif) -->
<p align="center">
  <img src="https://github.com/slowdivesun/war-game/blob/master/gifs/bomb_2.gif" width=50% height=50%>
</p>
<p align="center">
  <em>Bomb Randomness and Animation</em>
</p>

<!-- ![](https://github.com/slowdivesun/war-game/blob/master/gifs/enemy_flip.gif) -->
<p align="center">
  <img src="https://github.com/slowdivesun/war-game/blob/master/gifs/enemy_flip.gif" width=50% height=50%>
</p>
<p align="center">
  <em>Enemy movements</em>
</p>
