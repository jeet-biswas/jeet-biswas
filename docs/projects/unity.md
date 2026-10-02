# Interactive prototypes in Unity

These projects explore input handling, physics, scene state, collision events,
and user feedback using C# and Unity. They are source-code prototypes; the profile
does not claim current downloadable releases or measured runtime performance.

## Endless Runner

[Repository](https://github.com/jeet-biswas/Endless-Runner-Game) |
[Player controller](https://github.com/jeet-biswas/Endless-Runner-Game/blob/57791043402225715c96d617f8454ce4b5f39717/Assets/Player_controller.cs)

The player controller coordinates three-lane movement, keyboard/swipe input,
jumping, sliding, gravity, and animation. Related components manage coin counts,
obstacle-triggered game over, randomized tile spawning, and audio. The source
records Unity editor version `6000.1.13f1`.

This is practice in making input, world events, and presentation agree on the
current game state.

## Smaller gameplay exercises

| Project | Main learning focus | Source |
|---|---|---|
| Flappy Bird | 2D impulse movement, collisions, score and restart | [Bird controller](https://github.com/jeet-biswas/flappy-bird-game-unity/blob/c84d799273444abbd22696b6241a2c9f2bfd2795/Assets/birds.cs) |
| Roll a Ball | Rigidbody movement, trigger pickups, count and win state | [Player controller](https://github.com/jeet-biswas/Roll-A-Ball/blob/6bcb359fe395b6247e3b7e307fe63330f4983cd7/Assets/Player_controller_script.cs) |
| Car game | Movement, collision/falling recovery, and distance score | [Player script](https://github.com/jeet-biswas/Unity-car-game/blob/fcf74460878e6006d2f341d16d1c39537918243a/Assets/player.cs) |

## How to read the code

Start with the player controller, identify which events change state, then follow
the score and restart logic. Check the project's editor version before opening
it locally, and test behavior in the editor rather than inferring correctness
from a screenshot or a script name.

[Back to profile](../../README.md)
