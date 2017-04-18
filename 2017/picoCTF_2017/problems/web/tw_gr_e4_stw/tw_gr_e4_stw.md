# TW\_GR\_E4\_STW
#### Writeup by intelagent

* **Web**
* *200 points*
* Many saw the fourth installment of Toaster Wars: Going Rogue as a return to grace after the relative mediocrity of the third. I'm just glad it was made at all. And hey, they added some nifty new online scoreboard features, too!


At this point in the Toaster Wars series it is pretty clear that we need to pickup a flag item and use it to get the flag.

The flag had been on the 5th floor for the previous problems so let's go to the fifth floor!

As we get to floor 4 we see that the staircase is blocked off by walls, great. Upon further inspection it becomes evident that we cannot go through walls or warp. Hmm...

Here is the code relevant to ascending floors:

```javascript
if(state.player.location.r == state.map.stairs.r && state.player.location.c == state.map.stairs.c){
	db.scoreboard[socket.id].floor++;
	prm = generator.generateFloor(db.scoreboard[socket.id].floor)
		.then((newState) => {
			if(newState.done){
				socket.emit("win");
				return Promise.all[db.commit(socket.id, {done: true, win: true}), initState];
			}

			newState.player.items = state.player.items;
			newState.player.stats = state.player.stats;
			newState.player.stats.modifiers = {};
			newState.player.attacks = state.player.attacks;
			state = newState;
			log[0].outcome.push({
				type: "floor",
				number: state.map.floor + "F"
			});
			state.enemies = state.enemies.filter(function(en){
				return !en.dead;
			});
		})
}
```

Whenever a player's location is equal to that of a staircase we increment the floor we are on. However, this is a clear race condition.

For those unfamiliar with race condtions, a race condition is
> an undesirable situation that occurs when a device or system attempts to perform two or more operations at the same time, but because of the nature of the device or system, the operations must be done in the proper sequence to be done correctly.Apr 29, 2015


So how can we get this code to be called multiple times? The client side has all sorts of delays and timeouts, so it will not be fast enough to call this code twice before our floor changes. However, we can change our location using this code:

```javascript
api("action", {
	type: "move",
	direction: moveDir
});
```

So if we go up to a staricase and call this function 3 times we can go into the staircase, back out of the staircase, and again back into the staircase. This causes `db.scoreboard[socket.id].floor++;` to be called 2 times, skipping a floor.

We can queue up the api calls in the console like so:

```javascript
api("action", {
	type: "move",
	direction: 6
});

api("action", {
	type: "move",
	direction: 2
});

api("action", {
	type: "move",
	direction: 6
});
```

Doing this on the third floor immediately shoots us up to the fifth floor where we can grab the flag:

`im_still_upset_you_dont_get_to_keep_the_cute_scarves_in_the_postgame_33afc86a6e39c906a4ae54caddbd0e8d`
